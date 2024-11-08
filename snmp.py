import asyncio

from pysnmp.hlapi.v3arch.asyncio import *


from properties.snmp_env import *


class SNMPManager:
    def __init__(self):
        self.__username = SNMP_USERNAME
        self.__auth_key = SNMP_AUTH_KEY
        self.__priv_key = SNMP_PRIV_KEY

    def getSnmpHost(self):
        return SNMP_HOST

    # SNMPv2c
    async def get_snmpv2c(self, oid):
        snmp_engine = SnmpEngine()
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmp_engine,
            CommunityData(communityName='public', communityIndex='cisco1',securityName='public'),
            await UdpTransportTarget.create((SNMP_HOST, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )

        res = []
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
        else:

            for oid, value in varBinds:
                if isinstance(value, OctetString):
                    value = value.asOctets().decode('utf-8')
                    res.append((oid, value))
                else:
                    res.append((oid, value))

        return res

    # SNMPv3
    async def get_snmpv3(self, oid):
        snmp_engine = SnmpEngine()
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmp_engine,
            UsmUserData(
                self.__username,
                authKey=self.__auth_key,
                authProtocol=usmHMACMD5AuthProtocol,
            ),
            await UdpTransportTarget.create((SNMP_HOST, 161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
        )

        res = []
        if errorIndication:
            print(errorIndication)
        elif errorStatus:
            print(
                "{} at {}".format(
                    errorStatus.prettyPrint(),
                    errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                )
            )
        else:

            for oid, value in varBinds:
                if isinstance(value, OctetString):
                    value = value.asOctets().decode('utf-8')
                    res.append((oid, value))
                else:
                    res.append((oid, value))

        return res




if __name__ == '__main__':
    nms = SNMPManager()

    async def main():
        for oid, value in await nms.get_snmpv2c('1.3.6.1.2.1.1.1.0'):
            print(oid, value)
        #
        # for oid, value in await nms.get_snmpv3('1.3.6.1.2.1.1.4.0'):
        #     print(oid, value)

    asyncio.run(main())
