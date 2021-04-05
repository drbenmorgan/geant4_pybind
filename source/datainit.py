R"(

"""Dataset initialization

This checks whether all datasets can be found and offers to download missing ones.

"""

import os
import tarfile
import urllib.request
import tempfile
import sys
from os.path import expanduser


def directory_contains(dir, subdir):
    for f in os.listdir(dir):
        if os.path.isdir(os.path.join(dir, f)) and os.path.basename(f) == subdir:
            return True
    return False


progress=0


def show_progress(block_num, block_size, total_size):
    global progress
    bar_width=50
    if block_num == 0:
        sys.stdout.write("[%s]" % (" " * bar_width))
        sys.stdout.flush()
        sys.stdout.write("\b" * (bar_width+1))

    downloaded=int(bar_width * block_num * block_size/total_size)
    if downloaded < bar_width:
        while progress < downloaded:
            sys.stdout.write("#")
            progress += 1
        sys.stdout.flush()
    else:
        while progress < bar_width:
            sys.stdout.write("#")
            progress += 1
        sys.stdout.write("\n")
        sys.stdout.flush()
        progress=0


def download_dataset(url, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

    print("Downloading data file:", url)
    temp=tempfile.mktemp()
    urllib.request.urlretrieve(url, temp, show_progress)
    tar=tarfile.open(temp)
    tar.extractall(directory)
    tar.close()
    os.remove(temp)


def ask_for_download(data_directory):
    print("One or more Geant4 datasets were not found.")
    answer=input("Would you like to download the missing ones? [Y/n] ")
    if answer.lower() == 'y' or answer.lower() == 'yes':
        print("Storing data sets at:", data_directory)
        return True
    else:
        return False


def init_datasets():
    data_directory=os.path.join(os.path.expanduser("~"), ".geant4_pybind")
    download_allowed=False

    datasets=[["G4ABLADATA", "G4ABLA3.1", "http://cern.ch/geant4-data/datasets/G4ABLA.3.1.tar.gz"],

                ["G4ENSDFSTATEDATA", "G4ENSDFSTATE2.3",
                 "http://cern.ch/geant4-data/datasets/G4ENSDFSTATE.2.3.tar.gz"],

                ["G4INCLDATA", "G4INCL1.0", "http://cern.ch/geant4-data/datasets/G4INCL.1.0.tar.gz"],

                ["G4LEDATA", "G4EMLOW7.13", "http://cern.ch/geant4-data/datasets/G4EMLOW.7.13.tar.gz"],

                ["G4LEVELGAMMADATA", "PhotonEvaporation5.7",
                 "http://cern.ch/geant4-data/datasets/G4PhotonEvaporation.5.7.tar.gz"],

                ["G4NEUTRONHPDATA", "G4NDL4.6", "http://cern.ch/geant4-data/datasets/G4NDL.4.6.tar.gz"],

                ["G4PARTICLEXSDATA", "G4PARTICLEXS3.1.1",
                 "http://cern.ch/geant4-data/datasets/G4PARTICLEXS.3.1.1.tar.gz"],

                ["G4PIIDATA", "G4PII1.3",  "http://cern.ch/geant4-data/datasets/G4PII.1.3.tar.gz"],

                ["G4RADIOACTIVEDATA", "RadioactiveDecay5.6",
                 "http://cern.ch/geant4-data/datasets/G4RadioactiveDecay.5.6.tar.gz"],

                ["G4SAIDXSDATA", "G4SAIDDATA2.0", "http://cern.ch/geant4-data/datasets/G4SAIDDATA.2.0.tar.gz"],

                ["G4REALSURFACEDATA", "RealSurface2.2", "http://cern.ch/geant4-data/datasets/G4RealSurface.2.2.tar.gz"]]

    for dataset in datasets:
        if not dataset[0] in os.environ:
            if not os.path.exists(data_directory) or not directory_contains(data_directory, dataset[1]):
                if download_allowed or ask_for_download(data_directory):
                    download_allowed=True
                    download_dataset(
                        dataset[2], data_directory)
                else:
                    return

            os.environ[dataset[0]]=os.path.join(data_directory, dataset[1])

init_datasets()

# )"
