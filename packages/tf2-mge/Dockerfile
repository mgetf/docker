ARG REGISTRY=ghcr.io
ARG TF2_SOURCEMOD_TAG=latest
FROM ${REGISTRY}/mgetf/tf2-sourcemod/i386:${TF2_SOURCEMOD_TAG}
LABEL maintainer="thmorriss@gmail.com"

COPY checksum.md5 .

ARG MGEMOD_PLUGIN_FILE_NAME=mge.zip
ARG MGEMOD_PLUGIN_VERSION=v0.2.2
ARG MGEMOD_PLUGIN_URL=https://github.com/mgetf/MGEmod_tournament/releases/download/${MGEMOD_PLUGIN_VERSION}/mge.zip
ARG SOURCEBANS_VERSION=1.6.4
ARG SOURCEBANS_FILE_NAME=sourcebans-pp-${SOURCEBANS_VERSION}.plugin-only.tar.gz
ARG SOURCEBANS_URL=https://github.com/sbpp/sourcebans-pp/releases/download/${SOURCEBANS_VERSION}/${SOURCEBANS_FILE_NAME}
ARG AFK_MANAGER_URL=https://www.sourcemod.net/vbcompiler.php?file_id=170330
ARG AFK_MANAGER_FILE_NAME=afk_manager4.smx

RUN rm "${SERVER_DIR}/tf/addons/sourcemod/plugins/"{funcommands,funvotes}.smx

# Download plugins
RUN \
  wget -nv "${MGEMOD_PLUGIN_URL}" -O "${MGEMOD_PLUGIN_FILE_NAME}" && \
  wget -nv "${SOURCEBANS_URL}" -O "${SOURCEBANS_FILE_NAME}" && \
  wget -nv "${AFK_MANAGER_URL}" -O "${AFK_MANAGER_FILE_NAME}"

# Verify checksums
RUN md5sum -c checksum.md5

# Install MGEmod
RUN unzip -q "${MGEMOD_PLUGIN_FILE_NAME}" -d "${SERVER_DIR}/tf"

# Install SourceBans
RUN tar xf "${SOURCEBANS_FILE_NAME}" -C "${SERVER_DIR}/tf"

# Move AFK Manager
RUN mv "${AFK_MANAGER_FILE_NAME}" "${SERVER_DIR}/tf/addons/sourcemod/plugins/${AFK_MANAGER_FILE_NAME}"

# Cleanup
RUN rm "${MGEMOD_PLUGIN_FILE_NAME}" "${SOURCEBANS_FILE_NAME}" "${AFK_MANAGER_FILE_NAME}" checksum.md5

ENV SELECTED_MAP="mge_training_v8_beta4b"

COPY server.cfg.template "${SERVER_DIR}/tf/cfg/server.cfg.template"
COPY mapcycle.txt.template "${SERVER_DIR}/tf/cfg/mapcycle.txt.template"
COPY afk_manager.cfg "${SERVER_DIR}/tf/cfg/sourcemod/afk_manager.cfg"
COPY afk_manager.phrases.txt "${SERVER_DIR}/tf/addons/sourcemod/translations/afk_manager.phrases.txt"
