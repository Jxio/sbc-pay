#!/bin/bash

# Fix for OpenShift random UID - bookworm's glibc is stricter about /etc/passwd lookups
if ! whoami &> /dev/null; then
  if [ -w /etc/passwd ]; then
    echo "pay:x:$(id -u):0:pay:/ftp-poller:/bin/bash" >> /etc/passwd
    echo "Added UID $(id -u) to /etc/passwd"
  fi
fi

function start_cron_jobs() {
  echo "Starting go-crond as a background task ..."
  CRON_CMD="go-crond -v --allow-unprivileged --include=cron/"
  exec ${CRON_CMD}
}

start_cron_jobs
