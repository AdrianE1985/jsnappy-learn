from lxml import etree
import os


class Parse:

    # generate snap files for devices based on given commands and rpc
    def generate_reply(self, test_file, dev, snap_files):
        self.command_list = []
        self.rpc_list = []
        self.test_included = []
        path = os.getcwd()
        for t in test_file['tests_include']:
            self.test_included.append(t)
            if t in test_file:
                if ('command' in test_file[t][0]):
                    command = test_file[t][0]['command']
                    self.command_list.append(command)
                    name = '_'.join(command.split())
                    dev.open()
                    rpc_reply = dev.rpc.cli(command, format='xml')
                    print "rpc reply:", etree.tostring(rpc_reply)
                    filename = snap_files + '_' + name + '.' + 'xml'
                    output_file = os.path.join(path, 'snapshots', filename)
                    with open(output_file, 'w') as f:
                        f.write(etree.tostring(rpc_reply))
                elif('rpc' in test_file[t][0]):
                    rpc = test_file[t][0]['rpc']
                    self.rpc_list.append(rpc)
                    dev.open()
                    rpc_reply = getattr(dev.rpc, rpc.replace('-', '_'))()
                    print "rpc reply:", etree.tostring(rpc_reply)
                    filename = snap_files + '_' + rpc + '.' + 'xml'
                    output_file = os.path.join(path, 'snapshots', filename)
                    with open(output_file, 'w') as f:
                        f.write(etree.tostring(rpc_reply))
            else:
                print "Test case:  %s  not defined !!!!" % t
