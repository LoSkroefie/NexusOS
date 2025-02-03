import psutil
import os
import subprocess
import json
from typing import Dict, List, Any
import logging

class SystemTools:
    """AI-powered system management tools."""
    
    def __init__(self):
        self.setup_logging()
        
    def setup_logging(self):
        self.logger = logging.getLogger('NexusAI.SystemTools')
        
    def analyze_system_performance(self) -> Dict[str, Any]:
        """Analyze system performance and provide AI-powered recommendations."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Analyze CPU usage patterns
            cpu_analysis = self._analyze_cpu_usage(cpu_percent)
            
            # Analyze memory usage
            memory_analysis = self._analyze_memory_usage(memory)
            
            # Analyze disk usage
            disk_analysis = self._analyze_disk_usage(disk)
            
            return {
                'cpu': cpu_analysis,
                'memory': memory_analysis,
                'disk': disk_analysis,
                'recommendations': self._generate_recommendations(
                    cpu_analysis,
                    memory_analysis,
                    disk_analysis
                )
            }
            
        except Exception as e:
            self.logger.error(f"Error analyzing system performance: {str(e)}")
            return {'error': str(e)}
            
    def optimize_system(self) -> Dict[str, Any]:
        """Perform AI-driven system optimization."""
        try:
            # Get current system state
            analysis = self.analyze_system_performance()
            
            optimizations = []
            
            # Optimize based on analysis
            if analysis['memory']['usage_percent'] > 80:
                optimizations.extend(self._optimize_memory())
                
            if analysis['cpu']['average_usage'] > 70:
                optimizations.extend(self._optimize_cpu())
                
            if analysis['disk']['usage_percent'] > 85:
                optimizations.extend(self._optimize_disk())
                
            return {
                'optimizations_performed': optimizations,
                'new_analysis': self.analyze_system_performance()
            }
            
        except Exception as e:
            self.logger.error(f"Error optimizing system: {str(e)}")
            return {'error': str(e)}
            
    def monitor_processes(self) -> List[Dict[str, Any]]:
        """Monitor and analyze running processes."""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.as_dict()
                    processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'cpu_percent': pinfo['cpu_percent'],
                        'memory_percent': pinfo['memory_percent'],
                        'status': self._analyze_process(pinfo)
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
                    
            return sorted(processes, 
                         key=lambda x: (x['cpu_percent'] or 0) + (x['memory_percent'] or 0),
                         reverse=True)
                         
        except Exception as e:
            self.logger.error(f"Error monitoring processes: {str(e)}")
            return []
            
    def _analyze_cpu_usage(self, cpu_percent: List[float]) -> Dict[str, Any]:
        """Analyze CPU usage patterns."""
        return {
            'average_usage': sum(cpu_percent) / len(cpu_percent),
            'per_core_usage': cpu_percent,
            'status': 'high' if any(x > 80 for x in cpu_percent) else 'normal'
        }
        
    def _analyze_memory_usage(self, memory) -> Dict[str, Any]:
        """Analyze memory usage patterns."""
        return {
            'total': memory.total,
            'available': memory.available,
            'usage_percent': memory.percent,
            'status': 'high' if memory.percent > 80 else 'normal'
        }
        
    def _analyze_disk_usage(self, disk) -> Dict[str, Any]:
        """Analyze disk usage patterns."""
        return {
            'total': disk.total,
            'used': disk.used,
            'free': disk.free,
            'usage_percent': disk.percent,
            'status': 'high' if disk.percent > 85 else 'normal'
        }
        
    def _generate_recommendations(self, cpu, memory, disk) -> List[str]:
        """Generate AI-powered system recommendations."""
        recommendations = []
        
        if cpu['status'] == 'high':
            recommendations.append("High CPU usage detected. Consider terminating resource-intensive processes.")
            
        if memory['status'] == 'high':
            recommendations.append("Memory usage is high. Consider closing unused applications.")
            
        if disk['status'] == 'high':
            recommendations.append("Disk space is running low. Consider cleaning temporary files.")
            
        return recommendations
        
    def _optimize_memory(self) -> List[str]:
        """Perform memory optimization."""
        optimizations = []
        
        # Clear system cache
        if os.name == 'posix':  # Linux/Unix
            subprocess.run(['sync; echo 3 > /proc/sys/vm/drop_caches'], shell=True)
            optimizations.append("Cleared system cache")
        elif os.name == 'nt':  # Windows
            subprocess.run(['powershell', 'Clear-RecycleBin', '-Force'], capture_output=True)
            optimizations.append("Cleared recycle bin")
            
        return optimizations
        
    def _optimize_cpu(self) -> List[str]:
        """Perform CPU optimization."""
        optimizations = []
        
        # Find and optimize CPU-intensive processes
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                if proc.cpu_percent() > 50:  # High CPU usage
                    proc.nice(10)  # Lower priority
                    optimizations.append(f"Reduced priority of process {proc.name()}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
                
        return optimizations
        
    def _optimize_disk(self) -> List[str]:
        """Perform disk optimization."""
        optimizations = []
        
        # Clean temporary files
        temp_dirs = []
        if os.name == 'nt':  # Windows
            temp_dirs.append(os.environ.get('TEMP'))
        else:  # Linux/Unix
            temp_dirs.append('/tmp')
            
        for temp_dir in temp_dirs:
            if temp_dir and os.path.exists(temp_dir):
                try:
                    for item in os.listdir(temp_dir):
                        item_path = os.path.join(temp_dir, item)
                        try:
                            if os.path.isfile(item_path):
                                os.unlink(item_path)
                            elif os.path.isdir(item_path):
                                os.rmdir(item_path)
                        except Exception:
                            pass
                    optimizations.append(f"Cleaned temporary files in {temp_dir}")
                except Exception as e:
                    self.logger.error(f"Error cleaning temp directory: {str(e)}")
                    
        return optimizations
        
    def _analyze_process(self, pinfo: Dict[str, Any]) -> str:
        """Analyze a single process and return its status."""
        cpu_percent = pinfo.get('cpu_percent', 0) or 0
        memory_percent = pinfo.get('memory_percent', 0) or 0
        
        if cpu_percent > 50 or memory_percent > 50:
            return 'high_usage'
        elif cpu_percent > 20 or memory_percent > 20:
            return 'moderate_usage'
        else:
            return 'normal'
