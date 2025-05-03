ARG REGISTRY=ghcr.io
ARG TF2_SOURCEMOD_TAG=latest
FROM ${REGISTRY}/mgetf/tf2-sourcemod/i386:${TF2_SOURCEMOD_TAG}
LABEL maintainer="thmorriss@gmail.com"

COPY checksum.md5 .

ARG MGEMOD_PLUGIN_FILE_NAME=mge.zip
ARG MGEMOD_PLUGIN_VERSION=v0.2.2
ARG MGEMOD_PLUGIN_URL=https://github.com/mgetf/MGEmod_tournament/releases/download/${MGEMOD_PLUGIN_VERSION}/mge.zip

RUN rm "${SERVER_DIR}/tf/addons/sourcemod/plugins/"{funcommands,funvotes}.smx

# Download plugins
RUN \
  export SOURCEBANS_FILE_NAME="sourcebans-pp-1.6.4.plugin-only.tar.gz" && \
  wget -nv "${MGEMOD_PLUGIN_URL}" && \
  wget -nv "https://github.com/sbpp/sourcebans-pp/releases/download/1.6.4/${SOURCEBANS_FILE_NAME}" && \
  wget -nv "https://www.sourcemod.net/vbcompiler.php?file_id=170330" -O "afk_manager4.smx"

# Verify checksums
RUN md5sum -c checksum.md5

# Install plugins
RUN \
  export SOURCEBANS_FILE_NAME="sourcebans-pp-1.6.4.plugin-only.tar.gz" && \
  unzip -q "${MGEMOD_PLUGIN_FILE_NAME}" -d "${SERVER_DIR}/tf" && \
  tar xf "${SOURCEBANS_FILE_NAME}" -C "${SERVER_DIR}/tf" && \
  mv "afk_manager4.smx" "${SERVER_DIR}/tf/addons/sourcemod/plugins/afk_manager4.smx"

# Cleanup
RUN \
  export SOURCEBANS_FILE_NAME="sourcebans-pp-1.6.4.plugin-only.tar.gz" && \
  rm "${MGEMOD_PLUGIN_FILE_NAME}" && \
  rm "${SOURCEBANS_FILE_NAME}" && \
  rm "checksum.md5"

ENV SELECTED_MAP="mge_training_v8_beta4b"

COPY server.cfg.template "${SERVER_DIR}/tf/cfg/server.cfg.template"
COPY mapcycle.txt.template "${SERVER_DIR}/tf/cfg/mapcycle.txt.template"
COPY afk_manager.cfg "${SERVER_DIR}/tf/cfg/sourcemod/afk_manager.cfg"
COPY afk_manager.phrases.txt "${SERVER_DIR}/tf/addons/sourcemod/translations/afk_manager.phrases.txt"
