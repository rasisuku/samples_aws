import boto3

__author__ = "Sukumar Sengottaiyan"
#This program is a sample program and for reference. Test before using it.
#sample program lists security groups attached to EC2 running in public subnet. ie subnet with internet gateway route ("igw-")
#***Warning***. Same security group may be attached to multiple EC2 in both public or private subnets. so, you need to analyze before deleting any security group

ec2 = boto3.resource('ec2')
ec2c = boto3.client('ec2')

def get_public_sub_nets():
    public_subnets = {}
    # find route table for sub net id. also find igw for route table.
    apicall = ec2c.describe_route_tables()
    #print("--------------")

    for routeTable in apicall['RouteTables']:
        #print("--------------routeTable")
        #print(routeTable)
        associations = routeTable['Associations']
        routes = routeTable['Routes']
        #print("$$$$$$$$$$$$$ -routes")
        #print(routes)

        for route in routes:
            if route['GatewayId'].startswith('igw-'):
                #print("IGW route. for public subnet")
                #print(route['GatewayId'])

                # process subnets and add it to dict/map
                # print("--------------associations")
                # print(associations)
                for association in associations:
                    #print("***********")
                    #print(association)
                    if 'SubnetId' in association:
                        subnet_id = association['SubnetId']
                        route_table_id = association['RouteTableId']
                        public_subnets[subnet_id] = route_table_id
                        #print("===============================================================")
                        #print(public_subnets)
                        # rt = ec2c.describe_route_tables(RouteTableIds=[route_table_id])
                        # print("rrrrrrrrrrrrr=describe route tables")
                        # print(str(rt))
                break

    print("Public subnets and corresponding route table: " + str(public_subnets))
    return public_subnets

def list_public_sec_groups_for_EC2():
    pub_subnets = get_public_sub_nets()
    res = ec2c.describe_instances()
    # print(str(res))
    # find subnet id for EC2
    for reserv in res['Reservations']:
        for inst in reserv['Instances']:
            print("============================================================")
            print("EC2 instance: " + str(inst['InstanceId']))
            sub_net_id = ''
            if 'SubnetId' in inst:
                sub_net_id = inst['SubnetId']
                print("Subnet Id: " + str(sub_net_id))
            if sub_net_id != '' and (sub_net_id in pub_subnets):
                if 'SecurityGroups' in inst:
                    # print(str(inst['SecurityGroups']))
                    print("Security groups: ")
                    for sec_grp in inst['SecurityGroups']:
                        print("     " + sec_grp['GroupName'])
    print("============================================================")


list_public_sec_groups_for_EC2()





