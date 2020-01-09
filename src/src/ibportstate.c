/*
 * Copyright (c) 2004-2009 Voltaire Inc.  All rights reserved.
 *
 * This software is available to you under a choice of one of two
 * licenses.  You may choose to be licensed under the terms of the GNU
 * General Public License (GPL) Version 2, available from the file
 * COPYING in the main directory of this source tree, or the
 * OpenIB.org BSD license below:
 *
 *     Redistribution and use in source and binary forms, with or
 *     without modification, are permitted provided that the following
 *     conditions are met:
 *
 *      - Redistributions of source code must retain the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer.
 *
 *      - Redistributions in binary form must reproduce the above
 *        copyright notice, this list of conditions and the following
 *        disclaimer in the documentation and/or other materials
 *        provided with the distribution.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
 * MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
 * BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
 * ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
 * CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 */

#if HAVE_CONFIG_H
#  include <config.h>
#endif				/* HAVE_CONFIG_H */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <getopt.h>

#include <infiniband/umad.h>
#include <infiniband/mad.h>

#include "ibdiag_common.h"

struct ibmad_port *srcport;

/*******************************************/

static int get_node_info(ib_portid_t * dest, uint8_t * data)
{
	int node_type;

	if (!smp_query_via(data, dest, IB_ATTR_NODE_INFO, 0, 0, srcport))
		return -1;

	node_type = mad_get_field(data, 0, IB_NODE_TYPE_F);
	if (node_type == IB_NODE_SWITCH)	/* Switch NodeType ? */
		return 0;
	else
		return 1;
}

static int get_port_info(ib_portid_t * dest, uint8_t * data, int portnum,
			 int port_op)
{
	char buf[2048];
	char val[64];

	if (!smp_query_via(data, dest, IB_ATTR_PORT_INFO, portnum, 0, srcport))
		return -1;

	if (port_op != 4) {
		mad_dump_portstates(buf, sizeof buf, data, sizeof data);
		mad_decode_field(data, IB_PORT_LINK_WIDTH_SUPPORTED_F, val);
		mad_dump_field(IB_PORT_LINK_WIDTH_SUPPORTED_F,
			       buf + strlen(buf), sizeof buf - strlen(buf),
			       val);
		sprintf(buf + strlen(buf), "%s", "\n");
		mad_decode_field(data, IB_PORT_LINK_WIDTH_ENABLED_F, val);
		mad_dump_field(IB_PORT_LINK_WIDTH_ENABLED_F, buf + strlen(buf),
			       sizeof buf - strlen(buf), val);
		sprintf(buf + strlen(buf), "%s", "\n");
		mad_decode_field(data, IB_PORT_LINK_WIDTH_ACTIVE_F, val);
		mad_dump_field(IB_PORT_LINK_WIDTH_ACTIVE_F, buf + strlen(buf),
			       sizeof buf - strlen(buf), val);
		sprintf(buf + strlen(buf), "%s", "\n");
		mad_decode_field(data, IB_PORT_LINK_SPEED_SUPPORTED_F, val);
		mad_dump_field(IB_PORT_LINK_SPEED_SUPPORTED_F,
			       buf + strlen(buf), sizeof buf - strlen(buf),
			       val);
		sprintf(buf + strlen(buf), "%s", "\n");
		mad_decode_field(data, IB_PORT_LINK_SPEED_ENABLED_F, val);
		mad_dump_field(IB_PORT_LINK_SPEED_ENABLED_F, buf + strlen(buf),
			       sizeof buf - strlen(buf), val);
		sprintf(buf + strlen(buf), "%s", "\n");
		mad_decode_field(data, IB_PORT_LINK_SPEED_ACTIVE_F, val);
		mad_dump_field(IB_PORT_LINK_SPEED_ACTIVE_F, buf + strlen(buf),
			       sizeof buf - strlen(buf), val);
		sprintf(buf + strlen(buf), "%s", "\n");
	} else {
		mad_decode_field(data, IB_PORT_LINK_SPEED_ENABLED_F, val);
		mad_dump_field(IB_PORT_LINK_SPEED_ENABLED_F, buf, sizeof buf,
			       val);
		sprintf(buf + strlen(buf), "%s", "\n");
	}

	printf("# Port info: %s port %d\n%s", portid2str(dest), portnum, buf);
	return 0;
}

static int set_port_info(ib_portid_t * dest, uint8_t * data, int portnum,
			 int port_op)
{
	char buf[2048];
	char val[64];

	if (!smp_set_via(data, dest, IB_ATTR_PORT_INFO, portnum, 0, srcport))
		return -1;

	if (port_op != 4)
		mad_dump_portstates(buf, sizeof buf, data, sizeof data);
	else {
		mad_decode_field(data, IB_PORT_LINK_SPEED_ENABLED_F, val);
		mad_dump_field(IB_PORT_LINK_SPEED_ENABLED_F, buf, sizeof buf,
			       val);
		sprintf(buf + strlen(buf), "%s", "\n");
	}

	printf("\nAfter PortInfo set:\n");
	printf("# Port info: %s port %d\n%s", portid2str(dest), portnum, buf);
	return 0;
}

static int get_link_width(int lwe, int lws)
{
	if (lwe == 255)
		return lws;
	else
		return lwe;
}

static int get_link_speed(int lse, int lss)
{
	if (lse == 15)
		return lss;
	else
		return lse;
}

static void validate_width(int width, int peerwidth, int lwa)
{
	if ((width & peerwidth & 0x8)) {
		if (lwa != 8)
			IBWARN
			    ("Peer ports operating at active width %d rather than 8 (12x)",
			     lwa);
	} else if ((width & peerwidth & 0x4)) {
		if (lwa != 4)
			IBWARN
			    ("Peer ports operating at active width %d rather than 4 (8x)",
			     lwa);
	} else if ((width & peerwidth & 0x2)) {
		if (lwa != 2)
			IBWARN
			    ("Peer ports operating at active width %d rather than 2 (4x)",
			     lwa);
	} else if ((width & peerwidth & 0x1)) {
		if (lwa != 1)
			IBWARN
			    ("Peer ports operating at active width %d rather than 1 (1x)",
			     lwa);
	}
}

static void validate_speed(int speed, int peerspeed, int lsa)
{
	if ((speed & peerspeed & 0x4)) {
		if (lsa != 4)
			IBWARN
			    ("Peer ports operating at active speed %d rather than  4 (10.0 Gbps)",
			     lsa);
	} else if ((speed & peerspeed & 0x2)) {
		if (lsa != 2)
			IBWARN
			    ("Peer ports operating at active speed %d rather than 2 (5.0 Gbps)",
			     lsa);
	} else if ((speed & peerspeed & 0x1)) {
		if (lsa != 1)
			IBWARN
			    ("Peer ports operating at active speed %d rather than 1 (2.5 Gbps)",
			     lsa);
	}
}

int main(int argc, char **argv)
{
	int mgmt_classes[3] =
	    { IB_SMI_CLASS, IB_SMI_DIRECT_CLASS, IB_SA_CLASS };
	ib_portid_t portid = { 0 };
	int err;
	int port_op = 0;	/* default to query */
	int speed = 15;
	int is_switch = 1;
	int state, physstate, lwe, lws, lwa, lse, lss, lsa;
	int peerlocalportnum, peerlwe, peerlws, peerlwa, peerlse, peerlss,
	    peerlsa;
	int width = 255, peerwidth, peerspeed;
	uint8_t data[IB_SMP_DATA_SIZE];
	ib_portid_t peerportid = { 0 };
	int portnum = 0;
	ib_portid_t selfportid = { 0 };
	int selfport = 0;

	char usage_args[] = "<dest dr_path|lid|guid> <portnum> [<op>]\n"
	    "\nSupported ops: enable, disable, reset, speed, width, query";
	const char *usage_examples[] = {
		"3 1 disable\t\t\t# by lid",
		"-G 0x2C9000100D051 1 enable\t# by guid",
		"-D 0 1\t\t\t# (query) by direct route",
		"3 1 reset\t\t\t# by lid",
		"3 1 speed 1\t\t\t# by lid",
		"3 1 width 1\t\t\t# by lid",
		NULL
	};

	ibdiag_process_opts(argc, argv, NULL, NULL, NULL, NULL,
			    usage_args, usage_examples);

	argc -= optind;
	argv += optind;

	if (argc < 2)
		ibdiag_show_usage();

	srcport = mad_rpc_open_port(ibd_ca, ibd_ca_port, mgmt_classes, 3);
	if (!srcport)
		IBERROR("Failed to open '%s' port '%d'", ibd_ca, ibd_ca_port);

	if (ib_resolve_portid_str_via(&portid, argv[0], ibd_dest_type,
				      ibd_sm_id, srcport) < 0)
		IBERROR("can't resolve destination port %s", argv[0]);

	if (argc > 1)
		portnum = strtol(argv[1], 0, 0);

	/* First, make sure it is a switch port if it is a "set" */
	if (argc >= 3) {
		if (!strcmp(argv[2], "enable"))
			port_op = 1;
		else if (!strcmp(argv[2], "disable"))
			port_op = 2;
		else if (!strcmp(argv[2], "reset"))
			port_op = 3;
		else if (!strcmp(argv[2], "speed")) {
			if (argc < 4)
				IBERROR
				    ("speed requires an additional parameter");
			port_op = 4;
			/* Parse speed value */
			speed = strtoul(argv[3], 0, 0);
			if (speed > 15)
				IBERROR("invalid speed value %d", speed);
		} else if (!strcmp(argv[2], "width")) {
			if (argc < 4)
				IBERROR
				    ("width requires an additional parameter");
			port_op = 5;
			/* Parse width value */
			width = strtoul(argv[3], 0, 0);
			if (width > 15 && width != 255)
				IBERROR("invalid width value %d", width);
		}
	}

	err = get_node_info(&portid, data);
	if (err < 0)
		IBERROR("smp query nodeinfo failed");
	if (err) {		/* not switch */
		if (port_op == 0)	/* query op */
			is_switch = 0;
		else if (port_op == 2)	/* disable */
			IBERROR("Node type not switch - disable not allowed");
	}

	if (port_op)
		printf("Initial PortInfo:\n");
	else
		printf("PortInfo:\n");
	err = get_port_info(&portid, data, portnum, port_op);
	if (err < 0)
		IBERROR("smp query portinfo failed");

	/* Only if one of the "set" options is chosen */
	if (port_op) {
		if ((port_op == 1) || (port_op == 3)) {	/* Enable or Reset port */
			mad_set_field(data, 0, IB_PORT_PHYS_STATE_F, 2);	/* Polling */
			mad_set_field(data, 0, IB_PORT_STATE_F, 0);	/* No Change */
		} else if (port_op == 2) {	/* Disable port */
			printf("Disable may be irreversible\n");
			mad_set_field(data, 0, IB_PORT_STATE_F, 1);	/* Down */
			mad_set_field(data, 0, IB_PORT_PHYS_STATE_F, 3);	/* Disabled */
		} else if (port_op == 4) {	/* Set speed */
			mad_set_field(data, 0, IB_PORT_LINK_SPEED_ENABLED_F,
				      speed);
			mad_set_field(data, 0, IB_PORT_STATE_F, 0);
			mad_set_field(data, 0, IB_PORT_PHYS_STATE_F, 0);
		} else if (port_op == 5) {	/* Set width */
			mad_set_field(data, 0, IB_PORT_LINK_WIDTH_ENABLED_F,
				      width);
			mad_set_field(data, 0, IB_PORT_STATE_F, 0);
			mad_set_field(data, 0, IB_PORT_PHYS_STATE_F, 0);
		}

		err = set_port_info(&portid, data, portnum, port_op);
		if (err < 0)
			IBERROR("smp set portinfo failed");
		/* query op - only compare peer port if switch port, exclude SP0 */
	} else if (is_switch && portnum) {
		/* Now, make sure PortState is Active */
		/* Or is PortPhysicalState LinkUp sufficient ? */
		mad_decode_field(data, IB_PORT_STATE_F, &state);
		mad_decode_field(data, IB_PORT_PHYS_STATE_F, &physstate);
		if (state == 4) {	/* Active */
			mad_decode_field(data, IB_PORT_LINK_WIDTH_ENABLED_F,
					 &lwe);
			mad_decode_field(data, IB_PORT_LINK_WIDTH_SUPPORTED_F,
					 &lws);
			mad_decode_field(data, IB_PORT_LINK_WIDTH_ACTIVE_F,
					 &lwa);
			mad_decode_field(data, IB_PORT_LINK_SPEED_SUPPORTED_F,
					 &lss);
			mad_decode_field(data, IB_PORT_LINK_SPEED_ACTIVE_F,
					 &lsa);
			mad_decode_field(data, IB_PORT_LINK_SPEED_ENABLED_F,
					 &lse);

			/* Setup portid for peer port */
			memcpy(&peerportid, &portid, sizeof(peerportid));
			peerportid.drpath.cnt = 1;
			peerportid.drpath.p[1] = (uint8_t) portnum;

			/* Set DrSLID to local lid */
			if (ib_resolve_self_via(&selfportid,
						&selfport, 0, srcport) < 0)
				IBERROR("could not resolve self");
			peerportid.drpath.drslid = (uint16_t) selfportid.lid;
			peerportid.drpath.drdlid = 0xffff;

			/* Get peer port NodeInfo to obtain peer port number */
			err = get_node_info(&peerportid, data);
			if (err < 0)
				IBERROR("smp query nodeinfo failed");

			mad_decode_field(data, IB_NODE_LOCAL_PORT_F,
					 &peerlocalportnum);

			printf("Peer PortInfo:\n");
			/* Get peer port characteristics */
			err =
			    get_port_info(&peerportid, data, peerlocalportnum,
					  port_op);
			if (err < 0)
				IBERROR("smp query peer portinfo failed");

			mad_decode_field(data, IB_PORT_LINK_WIDTH_ENABLED_F,
					 &peerlwe);
			mad_decode_field(data, IB_PORT_LINK_WIDTH_SUPPORTED_F,
					 &peerlws);
			mad_decode_field(data, IB_PORT_LINK_WIDTH_ACTIVE_F,
					 &peerlwa);
			mad_decode_field(data, IB_PORT_LINK_SPEED_SUPPORTED_F,
					 &peerlss);
			mad_decode_field(data, IB_PORT_LINK_SPEED_ACTIVE_F,
					 &peerlsa);
			mad_decode_field(data, IB_PORT_LINK_SPEED_ENABLED_F,
					 &peerlse);

			/* Now validate peer port characteristics */
			/* Examine Link Width */
			width = get_link_width(lwe, lws);
			peerwidth = get_link_width(peerlwe, peerlws);
			validate_width(width, peerwidth, lwa);

			/* Examine Link Speed */
			speed = get_link_speed(lse, lss);
			peerspeed = get_link_speed(peerlse, peerlss);
			validate_speed(speed, peerspeed, lsa);
		}
	}

	mad_rpc_close_port(srcport);
	exit(0);
}
