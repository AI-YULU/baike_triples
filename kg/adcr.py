# coding=utf-8
from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Nic180319"))
class Klg(object):
    #向neo4j添加实体
    def add_en_0(self,tx,name):
        tx.run("MERGE (a:Node {name: $name})",name = name)
    def add_en(self,name):
        with driver.session() as session:
            session.write_transaction(self.add_en_0,name)
    #向neo4j添加关系
    def add_rel_0(self,tx,en1,rel,en2):
        tx.run("MATCH (n1:Node{name:$en1}),(n2:Node{name:$en2})"
               "MERGE (n1)-[r:"+rel+"]->(n2)",en1=en1,en2=en2)
    def add_rel(self,en1,rel,en2):
        with driver.session() as session:
            session.write_transaction(self.add_rel_0,en1,rel,en2)
    #添加属性
    def add_att_0(self,tx,name,att_dict):
        for key in att_dict.keys():
            value = att_dict[key]
            tx.run("MATCH (n:Node{name:$name})"
               "SET n."+key+" = $value",name=name,value=value)
    def add_att(self,name,att_dict):
        with driver.session() as session:
            session.write_transaction(self.add_att_0,name,att_dict)
    #删除实体
    def delete_0(self,tx,name):
        tx.run("MATCH (n:Node{name:$name})"
               "DETACH DELETE n",name = name) #DETACH会无视该节点的关系
    def delete(self,name):
        with driver.session() as session:
            session.write_transaction(self.delete_0,name)

    #删除关系
    def delete_rel_0(self,tx,en1,rel,en2):
        tx.run('MATCH (n1:Node{name:$en1})-[r:'+rel+']->(n2:Node{name:$en2})'
               'DELETE r',en1=en1,en2=en2)
    def delete_rel(self,en1,rel,en2):
        with driver.session() as session:
            session.write_transaction(self.delete_rel_0,en1,rel,en2)

    #根据实体和关系查找实体，例如查找蛇纹玉的产地，find(driver,'蛇纹玉','产地')
    def find(self,driver,en1,relation):
        with driver.session() as session:
            relationship = relation
            entity1 = en1
            n = len(entity1)
            cypher_statement = 'MATCH (name1:Node)-[r:' +relationship+ ']->(name2:Node)\
                               WHERE SUBSTRING(name1.name,0,{0}) = "{1}" RETURN [name1.name,"{2}",\
                               name2.name]'.format(n,entity1,relationship)
            result = session.run(cypher_statement).value()
        return result
if __name__ == "__main__":
    a = Klg()
    a.add_en('叶莉')
    a.add_rel('姚明','妻子','叶莉')
    #a.delete('徐震')
    result = a.find(driver,'姚明','妻子')
    print(result)
    #a.delete_rel('功夫','导演','周星驰')
    a.add_att('黄晓明',{'职业':'演员'})



