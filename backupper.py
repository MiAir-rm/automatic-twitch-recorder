import datetime
import os
import logging

logger = logging.getLogger(__name__)


class Backupper:

    def __init__(self, streamer_dict, backup_cmd, file_path, time_formatter='%Y%m%d_%H%M%S'):
        self.streamer_dict = streamer_dict
        self.streamer = self.streamer_dict['user_info']['display_name']
        self.streamer_login = self.streamer_dict['user_info']['login']
        self.stream_title = self.streamer_dict['stream_info']['title']
        self.stream_quality = self.streamer_dict['preferred_quality']
        self.file_path = file_path
        self.backup_cmd = backup_cmd
        self.time_formatter = time_formatter

    def backup(self):
        backup_cmd = self._formatted_backup_cmd()
        logging.info('backup command is %s', backup_cmd)

        ret = os.system(backup_cmd)
        logging.info('result of %s is %d', backup_cmd, ret)

        if ret == 0:
            try:
                os.remove(self.file_path)
                logging.info('remove file %s', self.file_path)
            except NotImplementedError as e:
                pass
        else:
            logging.error('backup %s failed', self.backup_cmd)

        return backup_cmd

    def _formatted_backup_cmd(self):
        """
        format backup command
        Parameters
        ----------

        Returns
        -------
        Example
        -------
        rclone sync '%(backup_file)' remote:/backup/twitch/%(streamer_login)/%(time)/
        """
        backup_cmd = self.backup_cmd
        backup_cmd = backup_cmd.replace('%(backup_file)', self.file_path)
        backup_cmd = backup_cmd.replace('%(streamer_login)', self.streamer_login)
        time_str = datetime.datetime.now().strftime(self.time_formatter)
        backup_cmd = backup_cmd.replace('%(time)', time_str)
        return backup_cmd
