Imports System.IO.Ports
Imports System.Threading

Module main
    ' Librerias para el cursor
    Declare Function GetCursorPos Lib "user32" (ByRef lpPoint As POINTAPI) As Boolean
    Declare Function SetCursorPos Lib "user32" (ByVal x As Long, ByVal y As Long) As Long
    Public Structure POINTAPI
        Dim X_Pos As Integer
        Dim Y_Pos As Integer
    End Structure

    Dim Galileo As New SerialPort
    Dim msg As String
    Dim ports As New List(Of String)
    Dim readThread As New Thread(AddressOf Read)
    Dim _continue As Boolean
    Dim message As String
    Dim nport As Integer

    Sub Main()
        ' Vincular el cerrado de la APP:
        AddHandler AppDomain.CurrentDomain.ProcessExit, AddressOf main_ProcessExit
        ' Pantalla de bienvenida
        Console.WriteLine("----------------------------------------")
        Console.WriteLine("Bienvenido al configurador del MouseFlex")
        Console.WriteLine("----------------------------------------")
        ' Mostrar puertos seriales disponibles
        Console.WriteLine("Puertos seriales disponibles: ")
        GetSerialPortNames()
        ' Seleccionar el puerto serial
        Console.Write("Seleccione el puerto serial correspondiente al mouse: ")
        msg = Console.ReadLine()
        Console.WriteLine("")
        ' Verificar que el dato sea correcto
        Do While Not IsNumeric(msg)
            Console.WriteLine("Error. El dato no es un numero")
            Console.Write("Seleccione el puerto serial correspondiente al mouse: ")
            msg = Console.ReadLine()
            Console.WriteLine("")
        Loop
        ' Crear parametros del puerto serial
        nport = CInt(msg)
        msg = ports.Item(nport)
        Galileo.PortName = msg
        Galileo.BaudRate = 9600
        ' Abrir el puerto
        _continue = True
        OpenSerialPort(msg)
        ' Comenzar a leer
        readThread.Start()
        Console.WriteLine("Para finalizar la ejecucion, presione <q>...")
        ' Cerrado del app
        Do While _continue
            message = Console.ReadLine
            If message = "q" Then
                _continue = False
                readThread.Abort()
                closing()
                Exit Sub
            End If
        Loop
        'Salir
        readThread.Join()
        Environment.Exit(0)
    End Sub

    ' Enlista todos los puertos disponibles
    Sub GetSerialPortNames()
        Dim c As Integer
        c = 0
        For Each sp As String In My.Computer.Ports.SerialPortNames
            Console.WriteLine(CStr(c) + ". " + sp)
            ports.Add(sp)
            c = c + 1
        Next
    End Sub

    ' Abre el puerto serial
    Sub OpenSerialPort(port As String)
        If Not Galileo.IsOpen Then
            Galileo.Open()
            If Galileo.IsOpen() Then
                Console.WriteLine("El Galileo fue conectado")
            End If
        Else
            Console.WriteLine("No es posible establecer conexión. Presione Enter para salir")
            Console.ReadKey()
        End If
    End Sub

    ' Cierra el puerto serial
    Sub closing()
        Console.WriteLine("Cerrando puertos...")
        If Galileo.IsOpen Then
            Galileo.Close()
        End If
    End Sub

    ' Proceso de cerrado de la aplicacion
    Private Sub main_ProcessExit(sender As Object, e As EventArgs)
        If Galileo.IsOpen Then
            Galileo.Close()
        End If
    End Sub

    ' Tarea de lectura en segundo plano
    Sub Read()
        While _continue
            Try
                If Galileo.IsOpen Then
                    Dim message As String = Galileo.ReadLine()
                    descompose(message)
                    'Console.WriteLine(message)
                End If
            Catch generatedExceptionName As TimeoutException
            End Try
        End While
    End Sub

    ' Descomposicion del mensaje
    Sub descompose(reading As String)
        Dim elements() As String = reading.Split(",")
        ' Estructura: x, y, lb, rb
        Dim x As Integer = CInt(elements(0))
        Dim y As Integer = CInt(elements(1))

        If Not x = 0 Or Not y = 0 Then
            SetCursor(x, y)
        End If
    End Sub

    ' Movimiento del cursor
    Sub SetCursor(x As Integer, y As Integer)
        Dim pos As POINTAPI
        GetCursorPos(pos)
        ' Console.WriteLine(CStr(pos.X_Pos) + " " + CStr(pos.Y_Pos))
        ' Mover el cursor lo indicado
        SetCursorPos(pos.X_Pos + x, pos.Y_Pos + y)
    End Sub

End Module


