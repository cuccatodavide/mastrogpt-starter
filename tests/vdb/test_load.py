import sys
sys.path.append("packages/vdb/load")
import vdb, time

def test_vdb():
    args = {}

    db = vdb.VectorDB(args,'default')
    db.destroy('default')
    assert len(db.embed("hello world")) == 1024

    assert len(db.vector_search("hello")) == 0
    
    db.insert("Hello world")
    db.insert("This is a test")
    db.insert("This is another test")
    time.sleep(1)

    test = db.vector_search("test")
    assert len(test) == 3
    assert test[0][1].find("test") != -1

    hello = db.vector_search("hello")
    assert hello[0][1].find("Hello") != -1

    assert db.remove_by_substring("test") == 2
    db.insert('a test for the image id','-1')
    ident = db.vector_search("image")
    print(ident)
    assert ident[0][2] == '-1'
    db.remove_by_substring("test")




