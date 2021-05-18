set JAVA_HOME="C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2021.1\jbr"
SET CLASSPATH=.;.\antlr-4.9.2-complete.jar
"C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2021.1\jbr\bin\java" org.antlr.v4.Tool -Dlanguage=Python3 -visitor -no-listener %* 
