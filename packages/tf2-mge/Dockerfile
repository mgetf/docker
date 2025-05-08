ARG REGISTRY=ghcr.io
ARG TF2_SOURCEMOD_TAG=latest
FROM ${REGISTRY}/mgetf/tf2-sourcemod/i386:${TF2_SOURCEMOD_TAG}
LABEL maintainer="thmorriss@gmail.com"

COPY checksum.md5 .

ARG MGEMOD_PLUGIN_FILE_NAME=mge.zip
ARG MGEMOD_PLUGIN_VERSION=v0.2.4
ARG MGEMOD_PLUGIN_URL=https://github.com/mgetf/MGEmod_tournament/releases/download/${MGEMOD_PLUGIN_VERSION}/mge.zip

RUN rm "${SERVER_DIR}/tf/addons/sourcemod/plugins/"{funcommands,funvotes}.smx

RUN wget -nv "https://builds.limetech.io/files/accelerator-2.5.0-git138-cd575aa-linux.zip" -O "accelerator.zip"
RUN unzip -o "accelerator.zip" -d "${SERVER_DIR}/tf"

# Install MGEmod
# Download plugins

#RUN wget -nv "${MGEMOD_PLUGIN_URL}" -O "${MGEMOD_PLUGIN_FILE_NAME}"
#RUN unzip -o "${MGEMOD_PLUGIN_FILE_NAME}" -d "${SERVER_DIR}/tf"

# Cleanup
#RUN rm "${MGEMOD_PLUGIN_FILE_NAME}" checksum.md5

ENV SELECTED_MAP="mge_16badlands_v2"

COPY server.cfg.template "${SERVER_DIR}/tf/cfg/server.cfg.template"
COPY mapcycle.txt.template "${SERVER_DIR}/tf/cfg/mapcycle.txt.template"
