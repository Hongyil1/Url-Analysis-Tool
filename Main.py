import methods
from mpi4py import MPI
import time
import argparse
import csv
import os

start_time = time.time()
comm = MPI.COMM_WORLD
rank = comm.rank
# The size should be less than the number of website
size = comm.size

# initial the csv file
filednames = ['url', 'status_code', 'CMS']
with open("result.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, filednames)
    writer.writeheader()
with open("wrong.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, filednames)
    writer.writeheader()
with open("noDetect.csv", 'w') as csvfile:
    writer = csv.DictWriter(csvfile, filednames)
    writer.writeheader()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Choose the file name")
    parser.add_argument('-f', dest='file', help='Input the file name')
    results = parser.parse_args()

    input_file = results.file

    if rank == 0:
        with open(input_file) as f:
            for i , line in enumerate(f):
                if i % size == rank:
                    if len(line) > 0:
                        url = line
                        methods.test(url)

        print("**************** Rank:%d Finish ****************" % rank)

        # Receive the signal from other ranks
        count = size - 1
        for i in range(1, size):
            signal = comm.recv(source=i)
            count -= signal

        if count == 0:
            print("**************** ALL Finish ****************")
            # shutdown computer when finished
            # os.system('sudo shutdown now -h')



    for i in range(1, size):
        if rank == i:
            with open(input_file) as f:
                for j, line in enumerate(f):
                    if j % size == rank:
                        if len(line) > 0:
                            url = line
                            methods.test(url)
            # Send finish signal to rank 0
            comm.send(1, dest=0)
            print("**************** Rank:%d Finish ****************" % rank)
