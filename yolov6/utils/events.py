#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import yaml
import logging
import shutil

def set_logging(name=None):
    rank = int(os.getenv('RANK', -1))
    logging.basicConfig(format="%(message)s", level=logging.INFO if (rank in (-1, 0)) else logging.WARNING)
    return logging.getLogger(name)

LOGGER = set_logging(__name__)
NCOLS = shutil.get_terminal_size().columns

def load_yaml(file_path):
    """Load data from yaml file."""
    if isinstance(file_path, str):
        with open(file_path, errors='ignore') as f:
            data_dict = yaml.safe_load(f)
    return data_dict


def save_yaml(data_dict, save_path):
    """Save data to yaml file"""
    with open(save_path, 'w') as f:
        yaml.safe_dump(data_dict, f, sort_keys=False)


def write_tblog(tblogger, epoch, results, losses):
    """Display mAP and loss information to log."""
    tblogger.add_scalar("val/mAP@0.5", results[0], epoch + 1)
    tblogger.add_scalar("val/mAP@0.50:0.95", results[1], epoch + 1)
    
    tblogger.add_scalar("train/iou_loss", losses[0], epoch + 1)
    tblogger.add_scalar("train/l1_loss", losses[1], epoch + 1)
    tblogger.add_scalar("train/obj_loss", losses[2], epoch + 1)
    tblogger.add_scalar("train/cls_loss", losses[3], epoch + 1)
    
        
        
