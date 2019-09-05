FROM amancevice/pandas:0.23.4-python3

RUN pip install argparse \
                synapseclient \
                git+https://github.com/larssono/bridgeclient.git \
                git+https://github.com/Sage-Bionetworks/synapsebridgehelpers
RUN git clone --single-branch --branch udall-superusers https://github.com/Sage-Bionetworks/biaffect-cirrhosis /root/biaffect-cirrhosis
