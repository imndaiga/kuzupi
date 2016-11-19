from flask import current_app
from configparser import ConfigParser
import netifaces

Config = ConfigParser()
Config.read(current_app.config['CONF_PATH'])

def config_section(sectionname):
	sectiondict = {}
	options = Config.options(sectionname)
	for option in options:
		try:
			sectiondict[option] = Config.get(sectionname, option)
			if sectiondict[option] == '<please_input>':
				DebugPrint("skip: {}".format(option))
		except:
			print("exception on {}".format(option))
			sectiondict[option] = None
	return _validate_section(sectionname, sectiondict)

def _validate_section(sectionname, sectiondict):
	hw_mode_list = ['a','b','g','ad']
	ht_capab_list = ['LDPC','HT40-','HT40+','HT40','SMPS-STATIC','SMPS-DYNAMIC',
	'GF','SHORT-GI-20','SHORT-GI-40','TX-STBC','RX-STBC1','RX-STBC12','RX-STBC123',
	'DELAYED-BA','MAX-AMSDU-7935','DSSS_CCK-40','40-INTOLERANT','LSIG-TXOP-PROT']
	wpa_key_mgmt_list = ['WPA-PSK','WPA-EAP','WPA-PSK-SHA256','WPA-EAP-SHA256']
	rsn_pairwise_list = ['TKIP','CCMP']
	if sectionname == 'HOSTAPD':
		ht_capab_split = sectiondict['ht_capab'].split(',')
		wpa_key_mgmt_split = sectiondict['wpa_key_mgmt'].split(',')
		rsn_pairwise_split = sectiondict['rsn_pairwise'].split(',')
		interfaces = netifaces.interfaces()
		if str(sectiondict['interface']) not in interfaces:
			raise ValueError('interface not found.')
		if sectiondict['driver'] != 'nl80211':
			raise ValueError('sorry, {} untested.'.format(sectiondict['driver']))
		if sectiondict['hw_mode'] not in hw_mode_list:
			raise ValueError('{} mode not supported.'.format(sectiondict['hw_mode']))
		if int(sectiondict['channel']) < 1 or int(sectiondict['channel']) > 14:
			raise ValueError('invalid channel selection.')
		if int(sectiondict['ieee80211n']) not in (0,1):
			raise ValueError('invalid ieee80211n enable/disable value.')
		if int(sectiondict['wmm_enabled']) not in (0,1):
			raise ValueError('invalid wmm_enabled enable/disable value.')
		if int(sectiondict['macaddr_acl']) not in (0,1,2):
			raise ValueError('invalid macaddr_acl flag.')
		if int(sectiondict['auth_algs']) not in (0,1):
			raise ValueError('invalid auth_algs flag.')
		if int(sectiondict['ignore_broadcast_ssid']) not in (0,1,2):
			raise ValueError('invalid ignore_broadcast_ssid flag.')
		# wpa and auth_algs configuration flags are bit fields.
		if int(sectiondict['wpa']) not in (1,2,3):
			raise ValueError('invalid wpa flag.')
		if int(sectiondict['auth_algs']) not in (1,2,3):
			raise ValueError('invalid auth_algs flag.')
		# wpa_key_mgmt, rsn_pairwise and ht_capab are combination flags.
		for val in wpa_key_mgmt_split:
			if val not in wpa_key_mgmt_list:
				raise ValueError('invalid wpa_key_mgmt flag.')
		for val in rsn_pairwise_split:
			if val not in rsn_pairwise_list:
				raise ValueError('invalid rsn_pairwise flag.')
		for val in ht_capab_split:
			if val not in ht_capab_list:
				raise ValueError('invalid ht_capab flag.')
	elif sectionname == 'DNSMASQ':
		sectiondict['listen-address']
		sectiondict['bind-interfaces']
		sectiondict['server']
		sectiondict['domain-needed']
		sectiondict['bogus-priv']
		sectiondict['dhcp-range']
	return sectiondict