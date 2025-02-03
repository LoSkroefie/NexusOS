from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QPoint, QTimer, Property
from PyQt6.QtGui import QPainter, QColor, QPainterPath
import math

class GlowEffect:
    """Creates a pulsing glow effect for widgets."""
    
    def __init__(self, widget: QWidget):
        self.widget = widget
        self._glow_radius = 0
        self.animation = QPropertyAnimation(self, b"glow_radius")
        self.setup_animation()
        
    def setup_animation(self):
        """Setup the glow animation."""
        self.animation.setDuration(2000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(10)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.setLoopCount(-1)
        
    def start(self):
        """Start the glow animation."""
        self.animation.start()
        
    def stop(self):
        """Stop the glow animation."""
        self.animation.stop()
        
    def get_glow_radius(self):
        return self._glow_radius
        
    def set_glow_radius(self, radius):
        self._glow_radius = radius
        self.widget.update()
        
    glow_radius = Property(float, get_glow_radius, set_glow_radius)

class PulsingBackground(QWidget):
    """Creates a pulsing background effect."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self._pulse_opacity = 0
        self.animation = QPropertyAnimation(self, b"pulse_opacity")
        self.setup_animation()
        
    def setup_animation(self):
        """Setup the pulsing animation."""
        self.animation.setDuration(3000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(255)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutSine)
        self.animation.setLoopCount(-1)
        
    def start(self):
        """Start the pulsing animation."""
        self.animation.start()
        
    def stop(self):
        """Stop the pulsing animation."""
        self.animation.stop()
        
    def get_pulse_opacity(self):
        return self._pulse_opacity
        
    def set_pulse_opacity(self, opacity):
        self._pulse_opacity = opacity
        self.update()
        
    pulse_opacity = Property(int, get_pulse_opacity, set_pulse_opacity)
    
    def paintEvent(self, event):
        """Paint the pulsing background."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Create gradient background
        gradient = QLinearGradient(0, 0, self.width(), self.height())
        gradient.setColorAt(0, QColor(0, 20, 40))
        gradient.setColorAt(1, QColor(0, 40, 80))
        
        # Add pulsing effect
        pulse_color = QColor(0, 255, 255, self._pulse_opacity)
        painter.fillRect(self.rect(), gradient)
        painter.fillRect(self.rect(), pulse_color)

class MatrixRainEffect(QWidget):
    """Creates a Matrix-style rain effect in the background."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.chars = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_rain)
        
    def start(self):
        """Start the matrix rain effect."""
        self.timer.start(50)  # Update every 50ms
        
    def stop(self):
        """Stop the matrix rain effect."""
        self.timer.stop()
        
    def update_rain(self):
        """Update the matrix rain characters."""
        # Add new characters at random positions
        if len(self.chars) < 100:  # Limit the number of characters
            x = random.randint(0, self.width())
            self.chars.append({
                'x': x,
                'y': 0,
                'speed': random.randint(2, 5),
                'char': random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'),
                'opacity': 255
            })
            
        # Update existing characters
        for char in self.chars[:]:
            char['y'] += char['speed']
            char['opacity'] -= 2
            if char['y'] > self.height() or char['opacity'] <= 0:
                self.chars.remove(char)
                
        self.update()
        
    def paintEvent(self, event):
        """Paint the matrix rain effect."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        for char in self.chars:
            color = QColor(0, 255, 255, char['opacity'])
            painter.setPen(color)
            painter.drawText(char['x'], char['y'], char['char'])
