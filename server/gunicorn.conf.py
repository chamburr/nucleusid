from prometheus_flask_exporter.multiprocess import GunicornPrometheusMetrics

from server.utils.config import SERVER_HOST, SERVER_PORT, SERVER_WORKERS

bind = f"{SERVER_HOST}:{SERVER_PORT}"
workers = SERVER_WORKERS


def child_exit(_, worker):
    GunicornPrometheusMetrics.mark_process_dead_on_child_exit(worker.pid)
