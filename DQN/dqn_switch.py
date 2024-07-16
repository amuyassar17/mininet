# File: dqn_switch.py

import sys
import os

# Debug statement to check if torch is accessible
try:
    import torch
    print("PyTorch is installed:", torch.__version__)
except ModuleNotFoundError:
    print("PyTorch is not installed or not found in the current environment.")
    sys.exit(1)

import time
import logging

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER, CONFIG_DISPATCHER, set_ev_cls
from ryu.ofproto import ofproto_v1_3
from simple_switch_13 import SimpleSwitch13
from dqn import Agent

class DRLSwitch13(SimpleSwitch13):
    def __init__(self, *args, **kwargs):
        super(DRLSwitch13, self).__init__(*args, **kwargs)
        self.state_size = 4  # Sesuaikan dengan state yang digunakan
        self.action_size = 2  # Jumlah tindakan yang mungkin
        self.agent = Agent(self.state_size, self.action_size)
        self.batch_size = 32

        # Setup logging
        self.logger = logging.getLogger('DRLSwitch13')
        self.logger.setLevel(logging.INFO)
        fh = logging.FileHandler('network_metrics.log')
        fh.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(message)s')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        msg = ev.msg
        datapath = msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        in_port = msg.match['in_port']

        # Ambil state jaringan saat ini
        state = self.get_network_state()
        action = self.agent.act(state)

        # Lakukan tindakan yang dipilih oleh agen
        self.perform_action(action, ev)

        # Dapatkan metrik jaringan setelah tindakan
        next_state = self.get_network_state()
        reward = self.calculate_reward(next_state)

        # Logging metrics
        self.logger.info(f'State: {state}, Action: {action}, Reward: {reward}, Next State: {next_state}')

        # Ingat pengalaman agen
        self.agent.remember(state, action, reward, next_state, done=False)

        # Replay pengalaman agen untuk pelatihan
        if len(self.agent.memory) > self.batch_size:
            self.agent.replay(self.batch_size)

    def get_network_state(self):
        # Implementasikan fungsi untuk mendapatkan state jaringan
        # Contoh: return [latency, throughput, bandwidth, ...]
        return [0, 0, 0, 0]

    def perform_action(self, action, ev):
        # Implementasikan fungsi untuk melakukan tindakan yang dipilih agen
        pass

    def calculate_reward(self, next_state):
        # Implementasikan fungsi untuk menghitung reward berdasarkan next_state
        # Contoh: return throughput - latency
        return 0

