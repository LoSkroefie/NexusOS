import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QTextEdit, QLineEdit, QPushButton, QTabWidget,
                            QHBoxLayout, QLabel)
from PyQt6.QtGui import QFont, QTextCursor, QPalette, QColor
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
import psutil
from nexus_core.nexus_ai import NexusAI
from nexus_core.voice_processor import VoiceProcessor
from nexus_core.system_tools import SystemTools
from .visual_effects import GlowEffect, PulsingBackground, MatrixRainEffect

class TerminalTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.nexus_ai = NexusAI()
        self.system_tools = SystemTools()
        self.init_ui()
        self.setup_voice_processor()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Add Matrix rain effect
        self.matrix_effect = MatrixRainEffect(self)
        self.matrix_effect.start()
        
        # Add pulsing background
        self.bg_effect = PulsingBackground(self)
        self.bg_effect.start()
        
        # System stats panel
        stats_layout = QHBoxLayout()
        self.cpu_label = QLabel("CPU: 0%")
        self.memory_label = QLabel("RAM: 0%")
        self.disk_label = QLabel("Disk: 0%")
        
        for label in [self.cpu_label, self.memory_label, self.disk_label]:
            label.setStyleSheet("color: cyan; font-weight: bold;")
            stats_layout.addWidget(label)
        
        layout.addLayout(stats_layout)
        
        # Output area with futuristic styling
        self.output_area = QTextEdit(self)
        self.output_area.setFont(QFont("Consolas", 12))
        self.output_area.setReadOnly(True)
        self.apply_futuristic_style(self.output_area)
        
        # Add glow effect
        self.glow = GlowEffect(self.output_area)
        self.glow.start()
        
        layout.addWidget(self.output_area)
        
        # Command input with futuristic styling
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit(self)
        self.input_field.setFont(QFont("Consolas", 12))
        self.input_field.setPlaceholderText("Enter command or ask NexusAI...")
        self.input_field.returnPressed.connect(self.process_command)
        self.apply_futuristic_style(self.input_field)
        
        self.voice_button = QPushButton("🎤")
        self.voice_button.clicked.connect(self.toggle_voice_input)
        self.apply_futuristic_style(self.voice_button)
        
        input_layout.addWidget(self.input_field)
        input_layout.addWidget(self.voice_button)
        
        layout.addLayout(input_layout)
        
        self.setLayout(layout)
        
        # Initialize system monitoring
        self.start_system_monitoring()
        
    def setup_voice_processor(self):
        """Setup voice command processing."""
        self.voice_processor = VoiceProcessor(self.handle_voice_command)
        self.voice_active = False
        
    def toggle_voice_input(self):
        """Toggle voice input on/off."""
        if self.voice_active:
            self.voice_processor.stop_listening()
            self.voice_button.setText("🎤")
            self.voice_active = False
            self.output_area.append("Voice input disabled")
        else:
            self.voice_processor.start_listening()
            self.voice_button.setText("🎤 (Active)")
            self.voice_active = True
            self.output_area.append("Voice input enabled - Speak your command")
            
    def handle_voice_command(self, command: str):
        """Handle voice command from voice processor."""
        self.output_area.append(f"\n🎤 {command}")
        self.process_command(command)
        
    def apply_futuristic_style(self, widget):
        palette = widget.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(0, 20, 40))
        palette.setColor(QPalette.ColorRole.Text, QColor(0, 255, 255))
        widget.setPalette(palette)
        
        # Add glow effect
        widget.setStyleSheet("""
            QWidget {
                border: 1px solid cyan;
                border-radius: 5px;
                padding: 5px;
                background-color: rgba(0, 20, 40, 200);
                color: cyan;
            }
            QWidget:focus {
                border: 2px solid rgb(0, 255, 255);
                background-color: rgba(0, 30, 60, 200);
            }
        """)
        
    def start_system_monitoring(self):
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.update_system_stats)
        self.monitor_timer.start(2000)  # Update every 2 seconds
        
    @pyqtSlot()
    def update_system_stats(self):
        # Get system stats
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Update labels with glowing effect
        self.cpu_label.setText(f"CPU: {cpu_percent:.1f}%")
        self.memory_label.setText(f"RAM: {memory.percent:.1f}%")
        self.disk_label.setText(f"Disk: {disk.percent:.1f}%")
        
        # Analyze system performance
        analysis = self.system_tools.analyze_system_performance()
        
        # Show recommendations if needed
        if analysis.get('recommendations'):
            self.output_area.append("\n🤖 System Recommendations:")
            for rec in analysis['recommendations']:
                self.output_area.append(f"• {rec}")
        
    @pyqtSlot()
    def process_command(self, command=None):
        if not command:
            command = self.input_field.text().strip()
        if not command:
            return
            
        self.output_area.append(f"\n> {command}")
        self.input_field.clear()
        
        # Process special system commands
        if command.startswith("system"):
            if "analyze" in command:
                analysis = self.system_tools.analyze_system_performance()
                self.output_area.append("\n📊 System Analysis:")
                self.output_area.append(f"CPU Status: {analysis['cpu']['status']}")
                self.output_area.append(f"Memory Status: {analysis['memory']['status']}")
                self.output_area.append(f"Disk Status: {analysis['disk']['status']}")
                
            elif "optimize" in command:
                self.output_area.append("\n🔧 Optimizing system...")
                result = self.system_tools.optimize_system()
                for opt in result.get('optimizations_performed', []):
                    self.output_area.append(f"✓ {opt}")
                    
            elif "monitor" in command:
                processes = self.system_tools.monitor_processes()
                self.output_area.append("\n👀 Top Processes:")
                for proc in processes[:5]:  # Show top 5
                    self.output_area.append(
                        f"• {proc['name']}: CPU {proc['cpu_percent']}%, "
                        f"RAM {proc['memory_percent']}%"
                    )
        else:
            # Process command through NexusAI
            result = self.nexus_ai.process_request(command)
            
            if result["success"]:
                self.output_area.append(result["output"])
            else:
                self.output_area.append(f"Error: {result['error']}")
                
        # Scroll to bottom
        cursor = self.output_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.output_area.setTextCursor(cursor)

class NexusTerminal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("NexusOS Terminal")
        self.setGeometry(100, 100, 1000, 600)
        
        # Create tab widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        # Add initial tab
        self.add_new_tab()
        
        # Add new tab button
        self.tabs.setCornerWidget(self.create_new_tab_button())
        
        self.setCentralWidget(self.tabs)
        
        # Apply futuristic window style
        self.setStyleSheet("""
            QMainWindow {
                background-color: rgb(0, 10, 30);
            }
            QTabWidget::pane {
                border: 1px solid cyan;
                background-color: rgb(0, 20, 40);
            }
            QTabBar::tab {
                background-color: rgb(0, 30, 60);
                color: cyan;
                padding: 8px;
                margin: 2px;
            }
            QTabBar::tab:selected {
                background-color: rgb(0, 40, 80);
                border: 1px solid rgb(0, 255, 255);
            }
        """)
        
    def create_new_tab_button(self):
        btn = QPushButton("+")
        btn.clicked.connect(self.add_new_tab)
        btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(0, 40, 80);
                color: cyan;
                border: 1px solid cyan;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(0, 60, 100);
            }
        """)
        return btn
        
    @pyqtSlot()
    def add_new_tab(self):
        new_tab = TerminalTab()
        self.tabs.addTab(new_tab, f"Terminal {self.tabs.count() + 1}")
        
    @pyqtSlot(int)
    def close_tab(self, index):
        if self.tabs.count() > 1:  # Keep at least one tab open
            self.tabs.removeTab(index)

def main():
    app = QApplication(sys.argv)
    terminal = NexusTerminal()
    terminal.show()
    sys.exit(app.exec())
