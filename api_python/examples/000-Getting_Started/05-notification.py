#! /usr/bin/env python3

###
# KINOVA (R) KORTEX (TM)
#
# Copyright (c) 2018 Kinova inc. All rights reserved.
#
# This software may be modified and distributed under the
# terms of the BSD 3-Clause license.
#
# Refer to the LICENSE file for details.
#
###

import time

from jaco3_armbase.UDPTransport import UDPTransport
from jaco3_armbase.RouterClient import RouterClient, RouterClientSendOptions
from jaco3_armbase.SessionManager import SessionManager

from jaco3_armbase.autogen.client_stubs.DeviceConfigClientRpc import DeviceConfigClient
from jaco3_armbase.autogen.client_stubs.BaseClientRpc import BaseClient

from jaco3_armbase.autogen.messages import DeviceConfig_pb2, Session_pb2, Base_pb2

from jaco3_armbase.Exceptions.KException import KException
from google.protobuf import json_format

def example_notification(base_service):

    def notification_callback(data):
        print("****************************")
        print("* Callback function called *")
        print(json_format.MessageToJson(data))
        print("****************************")

    # Registering to user topic
    try:
        notif_handle = base_service.OnNotificationConfigurationChangeTopic(notification_callback, Base_pb2.NotificationOptions())
    except KException:
        print("Error occured user probably already exist")
    except Exception:
        print("Error occured")

    print("Notification ID : {0}".format(notif_handle.identifier))
    time.sleep(5)

    # Creating a user
    full_user_profile = Base_pb2.FullUserProfile()
    full_user_profile.user_profile.username = 'jcash'
    full_user_profile.user_profile.firstname = 'Johnny'
    full_user_profile.user_profile.lastname = 'Cash'
    full_user_profile.user_profile.application_data = "Custom Application Stuff"
    full_user_profile.password = "pwd"

    user_profile_handle = base_service.CreateUserProfile(full_user_profile)

    # At this point the callback should be call because an event occurs in user topic

    print("User {0} created with id : {1}".format(full_user_profile.user_profile.username, user_profile_handle.identifier))
    time.sleep(5)


if __name__ == "__main__":

    DEVICE_IP = "192.168.1.10"
    DEVICE_PORT = 10000

    transport = UDPTransport()
    transport.connect(DEVICE_IP, DEVICE_PORT)
    router = RouterClient(transport, lambda kException: print("Error during connection"))

    session_info = Session_pb2.CreateSessionInfo()
    session_info.username = 'admin'
    session_info.password = 'admin'
    session_info.session_inactivity_timeout = 600000 # 10 minutes
    session_info.connection_inactivity_timeout = 2000 # 2 second

    session_manager = SessionManager(router)
    session_manager.CreateSession(session_info)

    base_service = BaseClient(router)

    # example core
    example_notification(base_service)
