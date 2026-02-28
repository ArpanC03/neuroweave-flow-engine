"""
NeuroWeave Flow Engine - Keystroke Dynamics Tracker
Captures keystroke timing patterns for flow state analysis
Optimized for AMD Ryzen CPU
"""

import time
import json
from datetime import datetime
from pynput import keyboard
from collections import deque

class KeystrokeTracker:
    """
    Tracks keystroke timing, rhythm, and patterns to detect cognitive flow states.
    
    Features:
    - Inter-keystroke interval (IKI) measurement
    - Typing rhythm entropy calculation
    - Pause detection (>2s gaps indicate potential distraction)
    - Privacy-preserving: captures timing only, NOT content
    """
    
    def __init__(self, window_size=60):
        """
        Args:
            window_size (int): Time window in seconds for rhythm analysis
        """
        self.window_size = window_size
        self.keystroke_times = deque(maxlen=1000)
        self.pause_events = []
        self.session_start = time.time()
        
    def on_press(self, key):
        """Callback for keyboard press events"""
        current_time = time.time()
        self.keystroke_times.append(current_time)
        
        # Detect long pauses (potential flow disruption)
        if len(self.keystroke_times) >= 2:
            interval = current_time - self.keystroke_times[-2]
            if interval > 2.0:  # 2+ second pause
                self.pause_events.append({
                    'timestamp': current_time,
                    'duration': interval
                })
    
    def calculate_rhythm_score(self):
        """
        Calculate typing rhythm consistency (higher = more flow)
        Returns score 0-100
        """
        if len(self.keystroke_times) < 10:
            return 50  # Neutral score
        
        # Calculate inter-keystroke intervals
        intervals = []
        for i in range(1, len(self.keystroke_times)):
            intervals.append(self.keystroke_times[i] - self.keystroke_times[i-1])
        
        # Filter out extreme outliers (pauses > 5s)
        filtered = [x for x in intervals if x < 5.0]
        
        if not filtered:
            return 50
        
        # Calculate coefficient of variation (lower = more consistent = higher flow)
        import numpy as np
        mean_interval = np.mean(filtered)
        std_interval = np.std(filtered)
        
        if mean_interval == 0:
            return 50
        
        cv = std_interval / mean_interval
        
        # Map CV to flow score (CV < 0.5 = high flow, CV > 2 = low flow)
        flow_score = max(0, min(100, 100 - (cv * 40)))
        
        return round(flow_score, 2)
    
    def get_recent_stats(self, seconds=30):
        """Get keystroke statistics for recent time window"""
        now = time.time()
        recent_keystrokes = [t for t in self.keystroke_times if now - t <= seconds]
        
        if not recent_keystrokes:
            return {
                'count': 0,
                'rate': 0,
                'rhythm_score': 50,
                'long_pauses': 0
            }
        
        # Count long pauses in window
        recent_pauses = [p for p in self.pause_events if now - p['timestamp'] <= seconds]
        
        return {
            'count': len(recent_keystrokes),
            'rate': len(recent_keystrokes) / seconds * 60,  # keystrokes per minute
            'rhythm_score': self.calculate_rhythm_score(),
            'long_pauses': len(recent_pauses)
        }
    
    def save_session_data(self, filepath='keystroke_session.json'):
        """Save session data for analysis"""
        session_data = {
            'start_time': datetime.fromtimestamp(self.session_start).isoformat(),
            'duration_seconds': time.time() - self.session_start,
            'total_keystrokes': len(self.keystroke_times),
            'pause_events': self.pause_events,
            'final_rhythm_score': self.calculate_rhythm_score()
        }
        
        with open(filepath, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"✅ Session data saved to {filepath}")

def demo_tracker():
    """Demo function to test keystroke tracking"""
    print("🧠 NeuroWeave Keystroke Tracker - Demo Mode")
    print("=" * 50)
    print("Start typing to see real-time flow metrics...")
    print("Press ESC to stop tracking\n")
    
    tracker = KeystrokeTracker()
    
    def on_press(key):
        tracker.on_press(key)
        
        # Print stats every 10 keystrokes
        if len(tracker.keystroke_times) % 10 == 0:
            stats = tracker.get_recent_stats(30)
            print(f"📊 Last 30s: {stats['count']} keys | "
                  f"{stats['rate']:.1f} KPM | "
                  f"Flow: {stats['rhythm_score']}/100 | "
                  f"Pauses: {stats['long_pauses']}")
        
        # Stop on ESC
        if key == keyboard.Key.esc:
            return False
    
    # Start listener
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
    
    # Save session
    tracker.save_session_data()
    print("\n✨ Tracking session complete!")

if __name__ == "__main__":
    demo_tracker()

