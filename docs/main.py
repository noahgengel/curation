#!/usr/bin/env python

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START sample]
"""A sample app that uses GCS client to operate on bucket and file."""

# [START imports]
from __future__ import absolute_import

import os
import uuid
import sys


import cloudstorage
from google.appengine.api import app_identity

# what is this hack? why can't google have simple examples doing all these
# things. it's pretty standard
#import google
#google.__path__ = ['/home/apm470/src/bamboo-creek-172917/pmi-clone/docs/lib2/'] + google.__path__
# print google.__path__

from google.cloud import bigquery

import webapp2

# setting the environment variable and extra imports

dev_flag = True
source_filename = None

if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
    import subprocess
    from optparse import OptionParser
    parser.add_option("-f", "--file", dest="filename", 
            help="to copy data for dev server", metavar="FILE")
    #parser.add_option("-q", "--quiet",action="store_false", dest="verbose",
    #        default=True, help="don't print status messages to stdout")
    dev_flag = False

    (options,args) = parser.parse_args()
    source_filename = options.filename
    print "GETS HERE",source_filename


# copy a file to the local space for dev server

if source_filename is not None:
    bashCommand = "gsutil cp gs://bamboo-creek-synpuf-100/" + source_filename  + " ."
    
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()

    dir_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(dir_path + '/' + source_filename):
        raise RuntimeError("source_file doesn't exist")

    
# [END imports]


class bqFunctions:

    # BigQuery Utility functions
    def wait_for_job(self,job):
        while True:
            job.reload()

            if job.state == 'DONE':
                if job.error_result: 
                    raise RuntimeError(job.errors) 
                return 
            time.sleep(1)

    # BigQuery functions

    # [BEGIN load_data_from_file]
    # for dev_appserver I guess.
    def load_data_from_file(self,source, dataset_name='dataset_name',
            table_name='table_name'):
        bigquery_client = bigquery.Client()
        dataset = bigquery_client.dataset(dataset_name)
        table = dataset.table(table_name)

        # Reload the table to get the schema.
        table.reload()
                        
        with open(source_file_name, 'rb') as source_file:
            # This example uses CSV, but you can use other formats.
            job = table.upload_from_file( source_file, source_format='text/csv')

        self.wait_for_job(job)

        print('Loaded {} rows into {}:{}.'.format( job.output_rows, dataset_name, table_name))
        return table

    # [END load_data_from_file]

    # [BEGIN load_data_from_gcs]
    def load_data_from_gcs(self,
            source,dataset_name='dataset_name',table_name='table_name'):
        bigquery_client = bigquery.Client(project="bamboo-creek-172917")
        dataset = bigquery_client.dataset(dataset_name)
        table = dataset.table(table_name)
        job_name = str(uuid.uuid4())
        job = bigquery_client.load_table_from_storage( job_name, table, source)

        job.begin()

        wait_for_job(job)

        self.response.write('Loaded {} rows into {}:{}.'.format( job.output_rows, dataset_name, table_name))
        return table



class MainPage(webapp2.RequestHandler):
    """Main page for GCS demo application."""

# [START get_default_bucket]
    def get(self):
        bucket_name = os.environ.get(
            'BUCKET_NAME', app_identity.get_default_gcs_bucket_name())

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(
            'Demo GCS Application running from Version: {}\n'.format(
                os.environ['CURRENT_VERSION_ID']))
        self.response.write('Using bucket name: \n\n'.format(bucket_name))
# [END get_default_bucket]

        bucket = '/' + bucket_name
        filename = bucket + '/tester.csv'
        self.tmp_filenames_to_clean_up = []

        self.create_file(filename)
        self.response.write('\n\n')
        # self.load_data_from_gcs('gs:/' + filename)

# [START write]
    def create_file(self, filename):
        """Create a file."""

        self.response.write('Creating file {}\n'.format(filename))

        # The retry_params specified in the open call will override the default
        # retry params for this particular file handle.
        write_retry_params = cloudstorage.RetryParams(backoff_factor=1.1)
        with cloudstorage.open(
            filename, 'w', content_type='text/plain', options={
                'x-goog-meta-foo': 'foo', 'x-goog-meta-bar': 'bar'},
                retry_params=write_retry_params) as cloudstorage_file:
                    cloudstorage_file.write('abcde\n')
                    cloudstorage_file.write(('f'*1024+',')*4 + '\n')
        self.tmp_filenames_to_clean_up.append(filename)
# [END write]

# [START read]
    def read_file(self, filename):
        self.response.write(
            'Abbreviated file content (first line and last 1K):\n')

        with cloudstorage.open(filename) as cloudstorage_file:
            self.response.write(cloudstorage_file.readline())
            cloudstorage_file.seek(-1024, os.SEEK_END)
            self.response.write(cloudstorage_file.read())
# [END read]

    def stat_file(self, filename):
        self.response.write('File stat:\n')

        stat = cloudstorage.stat(filename)
        self.response.write(repr(stat))

    def create_files_for_list_bucket(self, bucket):
        self.response.write('Creating more files for listbucket...\n')
        filenames = [bucket + n for n in [
            '/foo1', '/foo2', '/bar', '/bar/1', '/bar/2', '/boo/']]
        for f in filenames:
            self.create_file(f)

# [START list_bucket]
    def list_bucket(self, bucket):
        """Create several files and paginate through them."""

        self.response.write('Listbucket result:\n')

        # Production apps should set page_size to a practical value.
        page_size = 1
        stats = cloudstorage.listbucket(bucket + '/foo', max_keys=page_size)
        while True:
            count = 0
            for stat in stats:
                count += 1
                self.response.write(repr(stat))
                self.response.write('\n')

            if count != page_size or count == 0:
                break
            stats = cloudstorage.listbucket(
                bucket + '/foo', max_keys=page_size, marker=stat.filename)
# [END list_bucket]

    def list_bucket_directory_mode(self, bucket):
        self.response.write('Listbucket directory mode result:\n')
        for stat in cloudstorage.listbucket(bucket + '/b', delimiter='/'):
            self.response.write(stat)
            self.response.write('\n')
            if stat.is_dir:
                for subdir_file in cloudstorage.listbucket(
                        stat.filename, delimiter='/'):
                    self.response.write('  {}'.format(subdir_file))
                    self.response.write('\n')

# [START delete_files]
    def delete_files(self):
        self.response.write('Deleting files...\n')
        for filename in self.tmp_filenames_to_clean_up:
            self.response.write('Deleting file {}\n'.format(filename))
            try:
                cloudstorage.delete(filename)
            except cloudstorage.NotFoundError:
                pass
# [END delete_files]

app = webapp2.WSGIApplication(
    [('/ch/', MainPage)], debug=True)
# [END sample]