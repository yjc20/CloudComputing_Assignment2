
# Assignment-2 COMP90024

FROM python
ENV HTTP_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV HTTPS_PROXY http://wwwproxy.unimelb.edu.au:8000/
ENV http_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV https_proxy http://wwwproxy.unimelb.edu.au:8000/
ENV no_proxy localhost,127.0.0.1,localaddress,172.16.0.0/12,.melbourne.rc.nectar.o>
RUN mkdir Harvester
COPY . ./Harvester/
RUN pip install -r ./Harvester/required_modules.txt
WORKDIR ./Harvester/
CMD python main.py
