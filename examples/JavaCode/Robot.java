package frc.robot;

import edu.wpi.first.wpilibj.TimedRobot;
import edu.wpi.first.hal.CANData;
import edu.wpi.first.wpilibj.CAN;
import edu.wpi.first.wpilibj.smartdashboard.SendableChooser;
import edu.wpi.first.wpilibj.smartdashboard.SmartDashboard;

public class Robot extends TimedRobot {
  private CAN openmv;
  private CANData data;
  private Integer counter;

  @Override
  public void robotInit() 
  {
    //SmartDashboard.putData("Auto choices", m_chooser);
    System.out.println("robotInit");
    openmv = new CAN(3, 170, 12);
    data = new CANData();
    counter = 0;
  }


  @Override
  public void robotPeriodic() 
  {
    counter = counter + 1;
     if (counter == 50) {
       System.out.println("robotPeriodic");
       byte[] cmd = {'D', 'O', ' ', 'I', 'T', '!'};
       openmv.writePacket(cmd, 8);
       counter = 0;
     }
     
     boolean canCam = openmv.readPacketNew(4, data);
     if(canCam == true)
      {
        System.out.print(data.length);
        System.out.print(" = ");
        String outstr = new String(data.data);
        System.out.println(outstr);
      }
  }

  @Override
  public void autonomousInit() 
  {
    System.out.println("autonomousInit");
  }

  @Override
  public void autonomousPeriodic() 
  {
    System.out.println("autunomousPeriodic");
  }

  @Override
  public void teleopPeriodic() 
  {
    System.out.println("teleopPeriodic");
  }

  @Override
  public void testPeriodic() 
    {
    System.out.println("testPeriodic");
  }
}
