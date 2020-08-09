#!/bin/bash

for ((i=1; i<=20; i++))
do
    python experiments/pretrain_experiment/generate/generate_data.py
done