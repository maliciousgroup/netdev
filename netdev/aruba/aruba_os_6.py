"""Subclass specific to Aruba AOS 6.x"""

import re

from ..ios_like import IOSLikeDevice
from ..logger import logger


class ArubaAOS6(IOSLikeDevice):
    """Class for working with Aruba OS 6.X"""

    _disable_paging_command = 'no paging'
    """Command for disabling paging"""

    _config_exit = 'exit'
    """Command for existing from configuration mode to privilege exec"""

    _config_check = ') (config'
    """Checking string in prompt. If it's exist im prompt - we are in configuration mode"""

    _pattern = r"\({}.*?\) (\(.*?\))?\s?[{}]"
    """Pattern for using in reading buffer. When it found processing ends"""

    async def _set_base_prompt(self):
        """
        Setting two important vars:

            base_prompt - textual prompt in CLI (usually hostname)
            base_pattern - regexp for finding the end of command. It's platform specific parameter

        For Aruba AOS 6 devices base_pattern is "(prompt) (\(.*?\))?\s?[#|>]
        """
        logger.info("Host {}: Setting base prompt".format(self._host))
        prompt = await self._find_prompt()

        # Strip off trailing terminator
        self._base_prompt = prompt[1:-3]
        delimiters = map(re.escape, type(self)._delimiter_list)
        delimiters = r"|".join(delimiters)
        base_prompt = re.escape(self._base_prompt[:12])
        pattern = type(self)._pattern
        self._base_pattern = pattern.format(base_prompt, delimiters)
        logger.debug("Host {}: Base Prompt: {}".format(self._host, self._base_prompt))
        logger.debug("Host {}: Base Pattern: {}".format(self._host, self._base_pattern))
        return self._base_prompt

    async def exit_config_mode(self):
        """Exit from configuration mode"""
        logger.info('Host {}: Exiting from configuration mode'.format(self._host))
        output = ''
        exit_config = type(self)._config_exit
        # Considering max 3 level of submode in config mode
        for i in range(3):
            if await self.check_config_mode():
                self._stdin.write(self._normalize_cmd(exit_config))
                output += await self._read_until_prompt()
            else:
                return output

        if await self.check_config_mode():
            raise ValueError("Failed to exit from configuration mode")

        return output
