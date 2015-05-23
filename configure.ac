AC_INIT([pygroot], [1.0], [keldzh@gmail.com])
AC_CONFIG_AUX_DIR([config])
AM_INIT_AUTOMAKE([-Wall dist-bzip2 dist-zip no-dist-gzip foreign])
AM_PATH_PYTHON([3.2])
AX_PYTHON_MODULE([unittest2])
AM_CONDITIONAL([UNITTEST2], [test x$HAVE_PYMOD_UNITTEST2 = no])
AC_CONFIG_FILES([Makefile doc/Makefile src/Makefile tests/Makefile src/config.py])
AC_OUTPUT
