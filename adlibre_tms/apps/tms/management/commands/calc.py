import os
import shutil
import subprocess

from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings



class Command(BaseCommand):

    def __init__(self):
        BaseCommand.__init__(self)
        self.option_list += (
            make_option(
                '--quiet', '-q',
                default=False,
                action='store_true',
                help='Hide all command output.'),
        )
        self.option_list += (
            make_option(
                '--prod-indexes', '-p',
                default=False,
                action='store_true',
                help=''),
        )

    help = ""

    def handle(self, *args, **options):


        self.stdout.write('Finished!\n')
