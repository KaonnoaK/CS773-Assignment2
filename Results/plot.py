import re
import matplotlib.pyplot as plt
import numpy as np
import os

base_dir = 'base'
way_dir = 'dset'
sset_dir = 'sset'
dset_dir = 'dset'

file_pairs = [
    (os.path.join(base_dir, "base-1-1.txt"), os.path.join(way_dir, "dset-1-1.txt")),
    (os.path.join(base_dir, "base-1-2.txt"), os.path.join(way_dir, "dset-1-2.txt")),
    (os.path.join(base_dir, "base-2-2.txt"), os.path.join(way_dir, "dset-2-2.txt")),
    #(os.path.join(base_dir, "base-1-1.txt"), os.path.join(sset_dir, "sset-1-1.txt")),
    #(os.path.join(base_dir, "base-1-2.txt"), os.path.join(sset_dir, "sset-1-2.txt")),
    #(os.path.join(base_dir, "base-2-2.txt"), os.path.join(sset_dir, "sset-2-2.txt"))
    #(os.path.join(base_dir, "base-1-1.txt"), os.path.join(dset_dir, "dset-1-1.txt")),
    #(os.path.join(base_dir, "base-1-2.txt"), os.path.join(dset_dir, "dset-1-2.txt")),
    #(os.path.join(base_dir, "base-2-2.txt"), os.path.join(dset_dir, "dset-2-2.txt"))
]

bench_labels = ["mcf + mcf", "mcf + pearl", "pearl + pearl"]


def extract_ipcs(filename):
    with open(filename, 'r') as file:
        content = file.read()
    ipc_values = re.findall(r'cumulative IPC:\s*([\d.]+)', content)
    if len(ipc_values) >= 2:
        return float(ipc_values[-2]), float(ipc_values[-1])
    else:
        raise ValueError(f"Could not find IPCs in {filename}")


def extract_mpki(filename):
    with open(filename, 'r') as file:
        content = file.read()
    mpki_values = re.findall(r'MPKI:\s*([\d.]+)', content)
    if len(mpki_values) >= 2:
        return float(mpki_values[-2]), float(mpki_values[-1])
    else:
        raise ValueError(f"Could not find MPKIs in {filename}")



normalized_total_ipc = []
base_mpki_values = []
way_mpki_values = []

for base_file, way_file in file_pairs:
    base_cpu0, base_cpu1 = extract_ipcs(base_file)
    way_cpu0, way_cpu1 = extract_ipcs(way_file)
    base_total = base_cpu0 + base_cpu1
    way_total = way_cpu0 + way_cpu1
    norm_total = way_total / base_total if base_total else 0
    normalized_total_ipc.append(norm_total)
    
    base_mpki0, base_mpki1 = extract_mpki(base_file)
    way_mpki0, way_mpki1 = extract_mpki(way_file)
    avg_base_mpki = (base_mpki0 + base_mpki1) / 2
    avg_way_mpki = (way_mpki0 + way_mpki1) / 2
    base_mpki_values.append(avg_base_mpki)
    way_mpki_values.append(avg_way_mpki)

x = np.arange(len(bench_labels))
width = 0.35


fig, ax = plt.subplots(figsize=(7, 5))
rects = ax.bar(x, normalized_total_ipc, width, color='steelblue')
ax.set_ylabel('Normalized IPC', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(bench_labels, fontsize=11)
ax.set_ylim(0, 1.3)
ax.set_title('Normalized IPC (Way over Base)', fontsize=13)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('normalized_ipc.png', format='png', dpi=300)
plt.savefig('normalized_ipc.jpg', format='jpg', dpi=300)
plt.show()


fig, ax = plt.subplots(figsize=(7, 5))
rects1 = ax.bar(x - width/2, base_mpki_values, width, label='Non Secure System', color='steelblue')
rects2 = ax.bar(x + width/2, way_mpki_values, width, label='Secure System', color='indianred')
ax.set_ylabel('LLC MPKI', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(bench_labels, fontsize=11)
ax.set_title('LLC MPKI Comparison', fontsize=13)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('llc_mpki_comparison.png', format='png', dpi=300)
plt.savefig('llc_mpki_comparison.jpg', format='jpg', dpi=300)
plt.show()



def extract_self_evictions(filename):
    with open(filename, 'r') as file:
        content = file.read()
    selfevic_values = re.findall(r'Self[-\s]evictions\s*:\s*(\d+)', content, re.IGNORECASE)
    print(f"DEBUG {filename}: Found self-evictions -> {selfevic_values}")
    if len(selfevic_values) >= 2:
        return int(selfevic_values[-2]), int(selfevic_values[-1])
    elif len(selfevic_values) == 1:
        return int(selfevic_values[0]), 0
    else:
        raise ValueError(f"Could not find self-evictions in {filename}")


def extract_instructions(filename):
    with open(filename, 'r') as file:
        content = file.read()
    instructions_values = re.findall(r'Instructions:\s*(\d+)', content)
    if len(instructions_values) >= 2:
        return int(instructions_values[-2]), int(instructions_values[-1])
    else:
        raise ValueError(f"Could not find instructions in {filename}")


def extract_llc_misses(filename):
    with open(filename, 'r') as file:
        content = file.read()
    llc_miss_values = re.findall(r'LLC TOTAL\s+ACCESS:\s*\d+\s+HIT:\s*\d+\s+MISS:\s*(\d+)', content)
    print(f"DEBUG {filename}: Found self-evictions -> {llc_miss_values}")
    if len(llc_miss_values) >= 2:
        return int(llc_miss_values[-2]), int(llc_miss_values[-1])
    else:
        raise ValueError(f"Could not find LLC misses in {filename}")


base_sepki_values = []
way_sepki_values = []

for base_file, way_file in file_pairs:

    base_selfevic0, base_selfevic1 = extract_self_evictions(base_file)
    base_inst0, base_inst1 = extract_instructions(base_file)
    sepki_base_0 = (base_selfevic0 / base_inst0) * 1000 if base_inst0 else 0
    sepki_base_1 = (base_selfevic1 / base_inst1) * 1000 if base_inst1 else 0
    avg_base_sepki = (sepki_base_0 + sepki_base_1) / 2
    base_sepki_values.append(avg_base_sepki)

  
    way_llc_miss0, way_llc_miss1 = extract_llc_misses(way_file)
    way_inst0, way_inst1 = extract_instructions(way_file)
    sepki_way_0 = (way_llc_miss0 / way_inst0) * 1000 if way_inst0 else 0
    sepki_way_1 = (way_llc_miss1 / way_inst1) * 1000 if way_inst1 else 0
    avg_way_sepki = (sepki_way_0 + sepki_way_1) / 2
    way_sepki_values.append(avg_way_sepki)


fig, ax = plt.subplots(figsize=(7, 5))
rects1 = ax.bar(x - width/2, base_sepki_values, width, label='Non Secure System', color='steelblue')
rects2 = ax.bar(x + width/2, way_sepki_values, width, label='Secure System', color='indianred')
ax.set_ylabel('Self Evictions Per Kilo Instructions (SEPKI)', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(bench_labels, fontsize=11)
ax.set_title('Self Evictions Per Kilo Instructions (SEPKI) Comparison', fontsize=13)
ax.legend()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('sepki_comparison.png', format='png', dpi=300)
plt.savefig('sepki_comparison.jpg', format='jpg', dpi=300)
plt.show()

