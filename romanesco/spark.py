import six
import romanesco
import os
import sys

from ConfigParser import ConfigParser, NoOptionError


def setup_spark_env():
    # Setup pyspark
    try:
        spark_home = romanesco.config.get('spark', 'spark_home')

        # If not configured try the environment
        if not spark_home:
            spark_home = os.environ.get('SPARK_HOME')

        if not spark_home:
            raise Exception('spark_home must be set or SPARK_HOME must be set in '
                            'the environment')

        # Need to set SPARK_HOME
        os.environ['SPARK_HOME'] = spark_home

        if not os.path.exists(spark_home):
            raise Exception('spark_home is not a valid directory')
    except NoOptionError:
        raise Exception('spark_home must be configured')

    sys.path.append(os.path.join(spark_home, 'python'))
    sys.path.append(os.path.join(spark_home, 'bin'))

    # Check that we can import SparkContext
    try:
        from pyspark import SparkConf, SparkContext
    except Exception as ex:
        six.raise_from(Exception('Unable to create SparkContext, check Spark '
                                 'installation'), ex)


def create_spark_context(task_spark_conf):
    from pyspark import SparkConf, SparkContext
    # Set can spark configuration parameter user has specified
    spark_conf = SparkConf()
    for (name, value) in romanesco.config.items('spark'):
        spark_conf.set(name, value)

    # Override with any task specific configuration
    for (name, value) in task_spark_conf.items():
        spark_conf.set(name, value)

    # Build up the context, using the master URL
    sc = SparkContext(conf=spark_conf)

    return sc
