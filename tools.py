from platform import architecture, system
import os
import subprocess

arch_bit = architecture()[0]
arch_sys = "Windows" if "Windows" in architecture()[1] else architecture()[1]


def get_target_executable(exec: str):
    executable = os.path.join(os.getcwd(),
                              'tools', arch_bit, arch_sys,
                              exec if "Windows" not in arch_sys else exec + ".exe")
    return executable if os.path.isfile(executable) else None


mkvmerge = get_target_executable("mkvmerge")
mkvextract = get_target_executable("mkvextract")
mkvinfo = get_target_executable("mkvinfo")
curl = get_target_executable("curl")
