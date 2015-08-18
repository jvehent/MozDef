#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# Copyright (c) 2014 Mozilla Corporation
#
# Contributors:
# Michal Purzynski michal@mozilla.com

from lib.alerttask import AlertTask
import pyes

class AlertSSLBlacklistHit(AlertTask):
	def main(self):
		# look for events in last 15 mins
		date_timedelta = dict(minutes=15)
		# Configure filters using pyes
		must = [
			pyes.TermFilter('_type', 'bro'),
			pyes.TermFilter('eventsource', 'nsm'),
			pyes.TermFilter('category', 'brointel'),
			pyes.TermFilter('details.sources', 'abuse.ch SSLBL'),
			pyes.ExistsFilter('details.sourceipaddress')
		]
		self.filtersManual(date_timedelta, must=must)

		# Search events
		self.searchEventsSimple()
		self.walkEvents()

	# Set alert properties
	def onEvent(self, event):
		category = 'correlatedalerts'
		tags = ['nsm,bro,correlated']
		severity = 'NOTICE'
		hostname = event['_source']['hostname']

		# the summary of the alert is the same as the event
		summary = '{0} {1}'.format(hostname, event['_source']['summary'])

		# Create the alert object based on these properties
		return self.createAlertDict(summary, category, tags, [event], severity)

