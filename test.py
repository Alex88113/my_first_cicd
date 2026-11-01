from app import sum_

def test_sum():
    assert sum_(2, 6) == 8
    assert sum_(-1, 1) == 0
    print('All tests passed!")

if __name__ == "__main__":
    test_sum_()
