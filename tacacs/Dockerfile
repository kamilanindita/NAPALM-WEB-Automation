FROM ubuntu:18.04

RUN apt update && apt install tacacs+ -y

COPY tac_plus.conf /etc/tacacs+/tac_plus.conf

EXPOSE 49

CMD ["tac_plus", "-G", "-C", "/etc/tacacs+/tac_plus.conf"]
