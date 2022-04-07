# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 18:57:47 2022

@author: arjun
"""
import sys
import hashlib
import json
import os

filename = 'test_dump.sql'
#Path to MYSQL DUMP FILE

cmdstr = "peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile ${PWD}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n basic --peerAddresses localhost:7051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles ${PWD}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c \'"
#PATH TO CERTIFICATES


def parse(filename):
    
    with open(filename) as f:
        
        try:
            #print(f.read())
            return f
        
        except ValueError as e:
            print('invalid json: %s' % e)           
            sys.exit()

def table_init():
    
    
    
    #fileobj = parse(filename)
    
    #table_name = None
    
    with open(filename) as fileobj:
        
        inpdict = {}
        values = []
        for line in fileobj:
            
            if(line[:14] == "CREATE TABLE `"):
                table_name = line[14:-4]
                inpdict['table'] = table_name
                #call insert function
                
            if(line[:3] == "  `"):
                tstr = ""
                
                flag = 0
                
                for i in line:
                    if(i == "`"):
                        flag+=1
                    if(flag == 2):
                        break
                    
                    if(i != " " and i != "`"):
                        tstr = tstr + i
                
                values.append(tstr)
                #print(tstr)
                
                
                #print(inpdict)
            
            if(line[0] == ")"):
                inpdict["values"] = values
                #print(inpdict)
                #CALL FUNCTION TO ADD TO LEDGER
                encoded_query = json.dumps(inpdict).encode()
                queryHash = hashlib.sha256(encoded_query).hexdigest()
                queryString = encoded_query.decode()
                i = 0
                qs = "\\\""
                queryString = queryString.replace("\"", qs)
                global cmdstr
                cmdstr =  cmdstr + "{\"function\":\"CreateQuery\",\"Args\":[" + "\"" + queryHash + "\",\"" + queryString  + "\"]}" + "\'"
            
                print(cmdstr)
                os.system(cmdstr)
                inpdict = {}
                values = []
            
            if(line[:13] == "INSERT INTO `"):
                table_name = ""
                
                i = 13
                while(line[i] != ";"):
                    table_name += line[i]
                    i+=1
                    if(line[i] == "`"):
                        break
                #print(table_name)
                
                i = i + 9
                
                vstr = ""
                
                #print(line[i:])
                
                while(line[i] != ";"):
                    
                    #print(line[i])
                    
                    if(line[i] == "("):
                        vstr = ""
                    elif(line[i] == ")"):
                        vlist = vstr.split(",")
                        #print(vlist)
                        inpdict["table"] = table_name
                        inpdict["values"] = vlist
                        #print(inpdict)
                        encoded_query = json.dumps(inpdict).encode()
                        queryHash = hashlib.sha256(encoded_query).hexdigest()
                        queryString = encoded_query.decode()
                        i = 0
                        qs = "\\\""
                        queryString = queryString.replace("\"", qs)
                        cmdstr =  cmdstr + "{\"function\":\"CreateQuery\",\"Args\":[" + "\"" + queryHash + "\",\"" + queryString  + "\"]}" + "\'"
                    
                        #print(cmdstr)
                        os.system(cmdstr)
                        #call function to add to ledger
                        #print()
                    else:
                        vstr += line[i]
                        
                    i+=1 
                    '''vstr = ""
                        continue
                    
                    if(line[i] == ")"):
                        print(vstr)
                        break
                        
                    
                    vstr += line[i]
                    
                    print(vstr)
                    
                    i+=1    '''
                
                #vallist = line[i+9:-2].split(")")
                #print(vallist)
                #print()
                #for val in vallist:
                #    inpdict["table"] = table_name
                    
                    #vlist = val[]
                    #print(val[1:])
                    #print()
                #print()
            #print(inpdict)
        #print(table_name)
        

table_init()