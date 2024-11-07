# Task page 1 {id="NGsBGGMzMKPa"}

``` {#CSharpHelloWorld plugin="csPlugin" ideTask="t1" id="glG1Cy5mfAiQ"}
type: cs
filename: hello.cs
pointsRule:
    maxPoints: 2
    cumulative: true
    doc: 0.2
    run: 1.0
    test: 0.8
fullprogram: |!!
public class HelloWorld
{
    public static void Main()
    {
        // BYCODEBEGIN
        System.Console.WriteLine("Hello World");
        // BYCODEEND
    }
}
!!


postprogram: |!!
  data.points = 0.9;
  return data;
!!  
```

``` {#PythonHelloWorld plugin="csPlugin" ideTask="t2" id="zDLesD5M3Qqg"}
type: py
filename: animals.py
fullprogram: |!!
print("kissa istuu")
// BYCODEBEGIN
print("koira haukkuu")
// BYCODEEND
print("hevonen nauraa")
!!
ide_extra_files:
  - filename: kissa.txt
    content: |!!
    istuu 
    ja 
    naukuu
    !!
  - filename: koira.dat
    content: "seisoo ja haukkuu"
```

``` {#CSharpHelloWorld2 plugin="csPlugin" ideTask="t3" id="0FimvtLFFJYM"}
type: csharp
filename: hello.cs
fullprogram: |!!
public class HelloWorld
{
    public static void Main()
    {
        // BYCODEBEGIN
        System.Console.WriteLine("Hello World");
        // BYCODEEND
    }
}
!!
```
