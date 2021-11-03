# -*- coding: utf-8 -*-
# Copyright (c) 2021, Frappe and contributors
# For license information, please see license.txt

import frappe

from frappe.utils import now_datetime

def trigger():
	"""Will be triggered every 30 minutes"""
	# Get all ["Active", "Inactive"] sites
	# Trigger "Daily" frequency sites
	sites_with_daily_scheduled_updates = frappe.get_all(
		"Site", 
		filters={
			"status": ("in", ("Active", "Inactive")),
			"auto_updates_scheduled": True
		}, 
		fields=[
			"name",
			"auto_update_last_triggered_on",
			"update_trigger_time",
			"update_trigger_frequency"
		]
	)
	
	trigger_for_sites = list(filter(sites_with_daily_scheduled_updates, should_update_trigger))

	for site in trigger_for_sites:
		try:
			site_doc = frappe.get_doc("Site", site.name)
			site_doc.schedule_update()
			site_doc.auto_update_last_triggered_on = now_datetime()
			site_doc.save()
		except Exception:
			pass


def should_update_trigger(site):
	"""Returns `True` if the site update should be triggered"""
	# The update has never been triggered
	if not site.auto_update_last_triggered_on:
		return True

	# Return based on the set frequency
	if site.update_trigger_frequency == "Daily":
		return should_update_trigger_for_daily(site)
	elif site.update_trigger_frequency == "Weekly":
		return should_update_trigger_for_weekly(site)
	elif site.update_trigger_frequency == "Monthly":
		return should_update_trigger_for_monthly(site)

	return False
	

def should_update_trigger_for_daily(site):
	# now_time = now_datetime().time()
	# now_seconds = now_time.hour * 3600 + now_time.minute * 60 + now_time.second
	# site.update_trigger_time.seconds
	pass


def should_update_trigger_for_weekly(site):
	pass


def should_update_trigger_for_monthly(site):
	pass