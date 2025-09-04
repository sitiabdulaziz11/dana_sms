
def progress_context(request):
    """ Function to handel progress in steps
    """
    STEPS = [ "parent", "phone", "student", "emergency", "payment"]
    current_step = min(request.session.get("current_step", 1), len(STEPS))

    current_step = request.session.get("current_step", 1)
    total_steps = len(STEPS)
    progress_percent = int((current_step / total_steps) * 100) if total_steps > 0 else 0
    return {
        "current_step": current_step,
        "total_steps": total_steps,
        "progress_percent": progress_percent,
    }