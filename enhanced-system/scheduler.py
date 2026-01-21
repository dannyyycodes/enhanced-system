"""
Scheduler
=========
Runs workflows automatically at scheduled times
"""

import schedule
import time
import logging
from datetime import datetime
from config import Config
from workflow import WorkflowEngine


class AutomationScheduler:
    """Handles scheduled workflow runs"""
    
    def __init__(self):
        self.engine = WorkflowEngine()
        self.logger = logging.getLogger(__name__)
        self.is_running = False
    
    def setup_schedule(self):
        """Setup the schedule based on config"""
        schedule.clear()
        
        for slot in Config.POST_SCHEDULE:
            hour = slot['hour']
            minute = slot['minute']
            
            schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(
                self.scheduled_workflow_run
            )
            
            self.logger.info(f"📅 Scheduled: Daily at {hour:02d}:{minute:02d}")
    
    def scheduled_workflow_run(self):
        """Run workflow (called by scheduler)"""
        self.logger.info(f"⏰ Scheduled run triggered at {datetime.now()}")
        result = self.engine.run_workflow()
        
        if result['success']:
            self.logger.info("✅ Scheduled workflow completed")
        else:
            self.logger.error(f"❌ Scheduled workflow failed: {result['error']}")
        
        return result
    
    def run_now(self):
        """Manually trigger a workflow run"""
        self.logger.info("🚀 Manual run triggered")
        return self.engine.run_workflow()
    
    def start(self):
        """Start the scheduler"""
        if self.is_running:
            self.logger.warning("Scheduler already running")
            return
        
        self.is_running = True
        self.setup_schedule()
        
        self.logger.info("🤖 Automation Scheduler Started")
        self.logger.info(f"   Next run: {schedule.next_run()}")
        
        try:
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.logger.info("⏹️  Scheduler stopped by user")
        except Exception as e:
            self.logger.error(f"❌ Scheduler error: {e}")
        finally:
            self.is_running = False
    
    def stop(self):
        """Stop the scheduler"""
        self.is_running = False
        self.logger.info("⏹️  Scheduler stopping...")


if __name__ == '__main__':
    # Test the scheduler
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    scheduler = AutomationScheduler()
    
    print("\n🤖 Video Automation Scheduler")
    print("=" * 50)
    print("\nScheduled Times:")
    for slot in Config.POST_SCHEDULE:
        print(f"  • {slot['hour']:02d}:{slot['minute']:02d}")
    print("\nPress Ctrl+C to stop\n")
    print("=" * 50)
    
    scheduler.start()
