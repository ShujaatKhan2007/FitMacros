/**
 * WorkoutControls.jsx
 * --------------------
 * The control row shown during Coach Mode: navigate between exercises,
 * pause/resume the session, or end it early.
 */
export default function WorkoutControls({
  onPrevious,
  onNext,
  onPauseResume,
  isPaused,
  onEnd,
  canGoPrevious,
  canGoNext,
}) {
  return (
    <div className="workout-controls">
      <button
        type="button"
        className="workout-controls__button"
        onClick={onPrevious}
        disabled={!canGoPrevious}
      >
        ◀ Previous
      </button>
      <button type="button" className="workout-controls__button" onClick={onPauseResume}>
        {isPaused ? "▶ Resume" : "⏸ Pause"}
      </button>
      <button
        type="button"
        className="workout-controls__button"
        onClick={onNext}
        disabled={!canGoNext}
      >
        Next ▶
      </button>
      <button type="button" className="workout-controls__button workout-controls__button--end" onClick={onEnd}>
        End Workout
      </button>
    </div>
  );
}
