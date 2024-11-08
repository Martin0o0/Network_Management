from pysnmp.carrier.asyncio.dgram import udp
from pysnmp.entity import engine, config
from pysnmp.entity.rfc3413 import ntfrcv, cmdrsp
from pysnmp.proto.api import v2c



# SNMP Trap 수신을 위한 SNMP Engine 생성
snmp_engine = engine.SnmpEngine()

#UDP 기반의 162번 포트로 오는 모든 출처 허용
config.add_transport(snmp_engine, udp.DOMAIN_NAME, udp.UdpTransport().open_server_mode(("0.0.0.0", 162), ))

# Trap 및 notification 수신에 대한 설정

# SNMPv2c setup
config.add_v1_system(snmp_engine, "public", "public")


# SNMPv3/USM setup
# config.add_v3_user(
#     snmp_engine, 'nsone',
#     config.USM_AUTH_HMAC96_MD5, 'qwer1234',
#     securityName='nsone',
#     securityEngineId=v2c.OctetString(hexValue='800063A280D89403F900B200000001')
# )


def callbackForTrapOrInform(snmpEngine,  #CallBack Func
                            stateReference,
                            contextEngineId, contextName,
                            varBinds,
                            cbCtx):
    print('Notification from ContextEngineId "%s", ContextName "%s"' % (
        contextEngineId.prettyPrint(), contextName.prettyPrint()))
    for name, val in varBinds:
        print('%s = %s' % (name.prettyPrint(), val.prettyPrint()))




ntfrcv.NotificationReceiver(snmp_engine, callbackForTrapOrInform)  #수신 시 콜백 함수 설정

snmp_engine.transport_dispatcher.job_started(1)  #SNMP 엔진의 디스패처 작업 시작
#SNMP 디스패처는 이벤트를 수신하고 콜백함수를 호출하여 메시지를 처리하는 역할을 담당함
if __name__ == '__main__':
    print("시작")
    try:
        snmp_engine.open_dispatcher()  #메시지 수신 준비 및 비동기로 수신하며 콜백 함수 호출함
    except:
        snmp_engine.close_dispatcher()  # 수신 종료
        raise
