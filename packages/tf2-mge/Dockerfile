#FROM ${REGISTRY}/mgetf/tf2-sourcemod/i386:${TF2_SOURCEMOD_TAG}
FROM ghcr.io/melkortf/tf2-sourcemod/i386:latest

LABEL maintainer="thmorriss@gmail.com"

COPY checksum.md5 .

ARG MGEMOD_PLUGIN_FILE_NAME=mge.zip
ARG MGEMOD_PLUGIN_VERSION=v3.0.9
#ARG MGEMOD_PLUGIN_VERSION=v0.2.4
ARG MGEMOD_PLUGIN_URL=https://github.com/sapphonie/MGEMod/releases/download/${MGEMOD_PLUGIN_VERSION}/mge.zip
# ARG MGEMOD_PLUGIN_URL=https://github.com/mgetf/MGEmod_tournament/releases/download/${MGEMOD_PLUGIN_VERSION}/mge.zip

RUN rm "${SERVER_DIR}/tf/addons/sourcemod/plugins/"{funcommands,funvotes}.smx

# Install MGEmod
# Download plugins

RUN wget -nv "${MGEMOD_PLUGIN_URL}" -O "${MGEMOD_PLUGIN_FILE_NAME}"
RUN unzip -o "${MGEMOD_PLUGIN_FILE_NAME}" -d "${SERVER_DIR}/tf"

RUN wget -nv "https://github.com/mgetf/MGEmod_tournament/raw/refs/heads/master/maps/mge_granary_mid.bsp"
RUN wget -nv "https://github.com/mgetf/MGEmod_tournament/raw/refs/heads/master/maps/mge_16badlands_v2.bsp"
RUN mv mge_granary_mid.bsp "${SERVER_DIR}/tf/maps/"
RUN mv mge_16badlands_v2.bsp "${SERVER_DIR}/tf/maps/"

RUN wget -nv "https://raw.githubusercontent.com/mgetf/MGEmod_tournament/refs/heads/master/addons/sourcemod/configs/mgemod_spawns.cfg"
RUN mv mgemod_spawns.cfg "${SERVER_DIR}/tf/addons/sourcemod/configs/"

# Cleanup
#RUN rm "${MGEMOD_PLUGIN_FILE_NAME}" checksum.md5

ENV SELECTED_MAP="mge_granary_mid"
#ermt 

COPY server.cfg.template "${SERVER_DIR}/tf/cfg/server.cfg.template"
COPY mapcycle.txt.template "${SERVER_DIR}/tf/cfg/mapcycle.txt.template"
