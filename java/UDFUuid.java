package com.example.hive.udf;

import java.util.UUID;
import org.apache.hadoop.hive.ql.udf.UDFType;
import org.apache.hadoop.hive.ql.exec.Description;
import org.apache.hadoop.hive.ql.exec.UDF;
import org.apache.hadoop.io.Text;

@Description(name = "uuid", value = "_FUNC_()")
@UDFType(deterministic = false)
public class UDFUuid extends UDF {
        public Text evaluate() {
                return new Text(UUID.randomUUID().toString());
        }
}
