Overview
======
Within PFS instrument control, some part of hardware are operated standalone
without active control via an actor, such as UPS or ethernet switch, but we are
better to monitor some part of statuses from these devices in the MHS world to
be used from upper controller, such that operational conditions might be used
by the master controller/sequencer to check whether sequence can be processed
or not especially in emergency.

Concepts and operational considerations
======
Rough concept of this actor is to proxy SNMP values to the MHS world, not all
values but selected ones which are required for automated instrument operation
and management. Some other SNMP values are required to be archived as system
monitoring, and these could be pushed to the MHS world depends on what kind
of integrated system we will use for monitoring, archiving, and alerting, but
set as not in a (basic level of) scope of this actor.
Number of target devices might change over the entire instrument operation
period, and monitoring of some devices need to be kept running to later phase
of power failure modes after main part of infrastructure at CB2F going down, it
is better to design the system to run multiple instances of this actor over the
entire instrument. Although we need to run multiple instances of this actor, we
may want to query multiple SNMP targets from one instance, and design of code
need to be capable of such operation. Although as well known, running multiple
instances from one code base will be taken care by actorcore library, such as
handling of hostname (or instance name of actor), we need to keep these in mind
on configurations and deployment.

Considering operation using statuses pushed from instances of this actor, we
need to fix mapping of physical to pair of actor name and status name/id, also
it may be better to push their name in parallel to statuses like once at each
invoke point of instance (no need to push periodically, since the MHS server
will keep the last value, also mapping will/should not change during operation
on demand if we do such operation scheme). On the other hand, keeping mappings
statistically is also important for archive of statuses, we shall put a
regulation not to reuse instance names and status names (incl sequential IDs
within one instance), in any case. Status lines could be organized as one line
(one entry of KeysDictionary) per one target SNMP server, but also multiple
lines could be possible. There seems no difference on both pushing to the MHS
server and using in other actors, their organization could be up to each target
SNMP server (device).
It could be better for this actor to accept some commands, such as changing
period of status update, but this actor will not need to consider of on-demand
change/update of a list of statuses to be pushed - not to make configurations
or archives messy, and keep simple as just having a flag of error to connect
a SNMP port to some configured target(s). This also could make software design
simple that we just can allocate multiple static threads at a time of invoking
an instance, but not to consider of dynamic threading or keeping timing among
threads.
For operation, this actor may need to have bi-directional connection to the
MHS server to accept command channel from the MHS server, but it is possible
to have multiple instance in one host with coordinated configuration (not to
use the same port numbers among instances). Their hosts could be VM guest(s)
since this actor will not have any direct connection to hardware (not over
ethernet), cost to have multiple (or number of) instances are low.

Requirements
======
This actor is required to

* Capable of multiple instances from configuration point of view
* Push SNMP values acquired from multiple SNMP servers as configured

  * Run one thread per one SNMP server
  * Report error of SNMP connection or acquisition per target server
  * Push names of target SNMP servers (devices) and values at startup

* Accept command through the MHS serve for running configuration

  * Capable to change period of status updates

Software design
======
This actor will take a design of simple python threading with configuration
as dict handed to thread(s) on invoke, and to run one thread per one target
SNMP server (device). Configuration dict will not be updated from each
thread but could be changed by the main thread, which accepts commands from
the MHS server, to change configuration(s) of operation by commanded from
external such as period between each update. With this model, we will not
need to have any interlock among threads except for shutting down (which
could be just a signal from system).
In each thread, one target SNMP server will be handled in the same manner,
like one period of SNMP values' acquisition, and the thread will push SNMP
values as status lines defined in configuration. To make configuration file
structure simple and not to make messy by long OIDs, this actor shall provide
some standard modules per targets, like UPS, PDU, or network switch.
Considering multiple instances from one VM guest, it should be configurable
of port number(s), but modification is need to be performed in actorcore but
not in this actor.
