#FROM ${REGISTRY}/mgetf/tf2-sourcemod/i386:${TF2_SOURCEMOD_TAG}
FROM ghcr.io/melkortf/tf2-sourcemod/i386:latest

LABEL maintainer="thmorriss@gmail.com"

COPY checksum.md5 .

ARG LADDER_PLUGIN_FILE_NAME=ladder.zip

ARG LADDER_PLUGIN_URL=https://github.com/mgetf/MGEmod_tournament/releases/download/v0.211.0/ladder.zip

RUN rm "${SERVER_DIR}/tf/addons/sourcemod/plugins/"{funcommands,funvotes}.smx

# Install MGEmod
# Download plugins

RUN wget -nv "${LADDER_PLUGIN_URL}" -O "${LADDER_PLUGIN_FILE_NAME}"
RUN unzip -o "${LADDER_PLUGIN_FILE_NAME}" -d "${SERVER_DIR}/tf"

RUN wget -nv "https://github.com/mgetf/MGEmod_tournament/raw/refs/heads/master/maps/mge_16badlands_v2.bsp"
RUN mv mge_16badlands_v2.bsp "${SERVER_DIR}/tf/maps/"

RUN wget -nv "https://raw.githubusercontent.com/mgetf/MGEmod_tournament/refs/heads/master/addons/sourcemod/configs/mgemod_spawns.cfg"
RUN mv mgemod_spawns.cfg "${SERVER_DIR}/tf/addons/sourcemod/configs/"

# Cleanup
#RUN rm "${MGEMOD_PLUGIN_FILE_NAME}" checksum.md5

ENV SELECTED_MAP="mge_16badlands_v2"
#ermt 

COPY server.cfg.template "${SERVER_DIR}/tf/cfg/server.cfg.template"
COPY mapcycle.txt.template "${SERVER_DIR}/tf/cfg/mapcycle.txt.template"
