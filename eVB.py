import math

class vEBTree:
    def high(self, x):
        return int(math.floor(x / self.lu))

    def low(self, x):
        return x % self.lu

    def index(self, x, y):
        return x * self.lu + y

    def __init__(self, u: int):
        self.u = 2              # minimum size
        while self.u < u:
            self.u <<= 1

        self.lu = 2 ** int(math.floor(math.log2(self.u) / 2))
        self.min = None
        self.max = None

        if self.u > 2:
            self.summary = None
            self.clusters = [None for x in range(self.high(self.u))]

    def insert(self, x):
        if x >= self.u:
            return False
        else:
            self.__insert(x)
            return True

    def __empty_insert(self, x):
        self.min = x
        self.max = x

    def __insert(self, x):
        if self.min is None:  # cluster is empty
            self.__empty_insert(x)
        else:
            if x < self.min:
                t = self.min
                self.min = x
                x = t
            if self.u > 2:     # u == 2 means the node is leaf node, which only has min and max, no need insert
                high = self.high(x)
                cluster = self.clusters[high]
                if cluster is None:
                    cluster = vEBTree(self.lu)
                    self.clusters[high] = cluster
                    if self.summary is None:
                        self.summary = vEBTree(self.lu)
                    self.summary.__insert(high)  # only update summary when cluster is created
                cluster.__insert(self.low(x))
            if x > self.max:
                self.max = x

    def predecessor(self, x):
        if self.u == 2:
            if x == 1 and self.min == 0:
                return 0
            else:
                return None
        elif self.max is not None and x > self.max:
            return self.max
        else:
            cluster = self.clusters[self.high(x)]
            if (cluster is not None and
                cluster.min is not None and
                cluster.min < self.low(x)):  # predecessor exist in this cluster
                return self.index(self.high(x), cluster.predecessor(self.low(x)))
            else:
                if self.summary:
                    pre_cluster = self.summary.predecessor(self.high(x))
                    if pre_cluster:
                        return self.index(pre_cluster, self.clusters[pre_cluster].max)
                    else:
                        if self.min is not None and x > self.min:
                            return self.min
                        else:
                            return None
                else:
                    return None

    def successor(self, x):
        if x >= self.u:
            return None
        if self.u == 2:
            if x == 0 and self.max == 1:
                return 1
            else:
                return None
        elif self.min is not None and x < self.min:
            return self.min
        else:
            cluster = self.clusters[self.high(x)]
            if (cluster is not None and
                cluster.max is not None and
                self.low(x) < cluster.max):  # remember compare low(x), not x
                return self.index(self.high(x), cluster.successor(self.low(x)))
            else:
                if self.summary:
                    next_cluster = self.summary.successor(self.high(x))
                    if next_cluster:
                        return self.index(next_cluster, self.clusters[next_cluster].min)
                    else:
                        return None
                else:
                    return None

    def member(self, x):
        if self.min is None:  # empty cluster
            return False
        if self.min == x or self.max == x:
            return True
        if self.u == 2:
            return False
        if x >= self.u:  # in case x is greater than u
            return False
        cluster = self.clusters[self.high(x)]
        if cluster:
            return cluster.member(self.low(x))
        else:
            return False

    def delete(self, x):
        if self.member(x):
            self.__delete(x)
            return True
        else:
            return False

    def __delete(self, x):
        if self.min == self.max:  # just one item
            self.min = None
            self.max = None
        elif self.u == 2:  # must be two items in this cluster
            if x == 0:
                self.min = 1
            else:
                self.min = 0
            self.max = self.min  # now min == max means only one item in the cluster
        else:
            if x == self.min:  # replace min with successor then remove the successor in cluster
                first_cluster = self.summary.min
                x = self.index(first_cluster, self.clusters[first_cluster].min)
                self.min = x

            high = self.high(x)
            cluster = self.clusters[high]
            cluster.__delete(self.low(x))

            # update max if x == self.max
            if cluster.min is None:
                self.summary.__delete(high)
                if x == self.max:  # need to find new max
                    if self.summary.max is None:  # means no item in the cluster or only self.min left
                        self.max = self.min
                    else:
                        self.max = self.index(self.summary.max, self.clusters[self.summary.max].max)
            else:
                if x == self.max:
                    self.max = self.index(high, cluster.max)

