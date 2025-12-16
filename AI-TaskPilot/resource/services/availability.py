from resource.models import ResourceAvailability


def get_latest_availability(resource):
    snapshot = resource.availability.order_by('-snapshot_time').first()
    if not snapshot:
        return None

    load_factor = snapshot.committed_hours / (
        snapshot.committed_hours + snapshot.available_hours
    )

    return {
        "available_hours": snapshot.available_hours,
        "committed_hours": snapshot.committed_hours,
        "availability_ratio": snapshot.available_hours / max(1, snapshot.committed_hours),
        "load_factor": load_factor
    }
