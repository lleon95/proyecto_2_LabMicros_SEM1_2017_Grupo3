Imports System.IO.Ports
Imports System.Threading

Module main
    ' Librerias para el cursor
    Declare Function GetCursorPos Lib "user32" (ByRef lpPoint As POINTAPI) As Boolean
    Declare Function SetCursorPos Lib "user32" (ByVal x As Long, ByVal y As Long) As Long
    Declare Auto Sub mouse_event Lib "user32" (ByVal dwFlags As Int32, ByVal dx As Int32, ByVal dy As Int32, ByVal cButtons As Int32, ByVal dwExtraInfo As IntPtr)
    Const MOUSEEVENTF_LEFTDOWN As Int32 = &H2 '  left button down
    Const MOUSEEVENTF_LEFTUP As Int32 = &H4 '  left button up
    Const MOUSEEVENTF_RIGHTDOWN As Int32 = &H8 '  right button down
    Const MOUSEEVENTF_RIGHTUP As Int32 = &H10 '  right button up

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

    Dim LB As Boolean
    Dim RB As Boolean

    Sub Main()
        ' Vincular el cerrado de la APP:
        AddHandler AppDomain.CurrentDomain.ProcessExit, AddressOf main_ProcessExit
        LB = False
        RB = False
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
        Galileo.BaudRate = 19200
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
    Dim startAttemps As Integer = 0
    Sub Read()
        While _continue
            Try
                If Galileo.IsOpen Then
                    Dim message As String = Galileo.ReadLine()
                    If startAttemps > 3 Then
                        descompose(message)
                    Else
                        startAttemps = startAttemps + 1
                    End If
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
        Dim clic As Integer = CInt(elements(2))

        If Not x = 0 Or Not y = 0 Then
            SetCursor(x, y)
        End If

        If clic > 0 Then
            If clic = 1 And LB = False Then
                mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                LB = True
            ElseIf clic = 2 And RB = False Then
                mouse_event(MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                RB = True
            ElseIf clic = 0 Then
                If RB = True Then
                    mouse_event(MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                    RB = False
                ElseIf LB = True Then
                    mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    LB = False
                End If

            End If
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


