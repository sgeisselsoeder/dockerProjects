#ifndef __JDAQUTCEXTENDED__
#define __JDAQUTCEXTENDED__

//#include <cstdint> // only in C++0x, will give uint32_t

#include "JDAQ/JDAQRoot.hh"
#include "JIO/JSerialisable.hh"
#include <iomanip>

namespace KM3NETDAQ {

  using JIO::JReader;
  using JIO::JWriter;


  /**
   * Data structure for UTC time.
   */
  class JDAQUTCExtended 
  {
  public:
  
    typedef unsigned int JUINT32_t; // preferably uint32_t


    /** 
     * Default constructor.
     */
    JDAQUTCExtended()
    {}


    /**
     * Constructor.
     *
     * \param  seconds     seconds [s]
     * \param  cycles      cycles [16 ns] 
     */    
    JDAQUTCExtended(const JUINT32_t seconds,
		    const JUINT32_t cycles):
      UTC_seconds(seconds),
      UTC_16nanosecondcycles(cycles)
    {}
   

    /**
     * Constructor.
     *
     * \param  nanoseconds time [ns]
     */    
    JDAQUTCExtended(const double nanoseconds)
    {
      setTimeNanoSecond(nanoseconds);
    }


    /** 
     * Virtual destructor.
     */
    virtual ~JDAQUTCExtended()
    {}
        

    /** 
     * Get time.
     *
     * \return             time [s]
     */
    JUINT32_t getUTCseconds() const
    {
      return UTC_seconds;
    }
        

    /** 
     * Get time.
     *
     * \return             time [16 ns]
     */
    JUINT32_t getUTC16nanosecondcycles() const
    {
      return UTC_16nanosecondcycles;
    }
        

    /** 
     * Get time (limited to 16 ns cycles).
     *
     * \return             time [ns]
     */
    double getTimeNanoSecond() const
    {
      return UTC_seconds*1.0e9 + UTC_16nanosecondcycles*16.0;
    }
    

    /** 
     * Set time.
     *
     * \param  utc_ext_ns  time [ns]
     */
    void setTimeNanoSecond(const double utc_ext_ns)
    {
      UTC_seconds            = (unsigned int) ( utc_ext_ns / 1.0e9);
      UTC_16nanosecondcycles = (unsigned int) ((utc_ext_ns - UTC_seconds*1.0e9) / 16.0);
    }
    

    /** 
     * Read UTCExtended from input
     *
     * \param  in          JReader
     * \param  utc_ext     JDAQUTCExtended
     * \return             JReader
     */
    friend inline JReader& operator>>(JReader& in, JDAQUTCExtended& utc_ext)
    {
      in >> utc_ext.UTC_seconds;
      in >> utc_ext.UTC_16nanosecondcycles;
       
      return in;
    }
    

    /** 
     * Write UTCExtended to output
     *
     * \param  out         JWriter
     * \param  utc_ext     JDAQUTCExtended
     * \return             JWriter
     */
    friend inline JWriter& operator<<(JWriter& out, const JDAQUTCExtended& utc_ext)
    {
      out << utc_ext.UTC_seconds;
      out << utc_ext.UTC_16nanosecondcycles;
           
      return out;
    }

     
    /**
     * Get size of object.
     *
     * \return             number of bytes
     */
    static int sizeOf()
    {
      return 2*sizeof(JUINT32_t);
    }
    

    ClassDef(JDAQUTCExtended,1);


  protected:
    JUINT32_t UTC_seconds;
    JUINT32_t UTC_16nanosecondcycles;
  };


  /**
   * Print UTC time.
   *
   * \param  out           output stream
   * \param  utc_ext       UTC extended time
   * \return               output stream
   */
  inline std::ostream& operator<<(std::ostream& out, const JDAQUTCExtended& utc_ext)
  {
    using namespace std;

    out << setw(10) << utc_ext.getUTCseconds();
    out << ':';
    out << setw(10) << setfill('0') << utc_ext.getUTC16nanosecondcycles() << setfill(' ');

    return out;
  }


  /**
   * Less than operator for UTC times.
   *
   * \param  first       UTC time
   * \param  second      UTC time
   * \result             true if first UTC time earlier than second UTC time; else false
   */
  inline bool operator<(const JDAQUTCExtended& first, const JDAQUTCExtended& second)
  {
    if (first.getUTCseconds() == second.getUTCseconds())
      return first.getUTC16nanosecondcycles() < second.getUTC16nanosecondcycles();
    else
      return first.getUTCseconds() < second.getUTCseconds();
  }

 
  /**
   * Equal operator for UTC times.
   *
   * \param  first       UTC time
   * \param  second      UTC time
   * \result             true if first UTC time equal second UTC time; else false
   */
  inline bool operator==(const JDAQUTCExtended& first, const JDAQUTCExtended& second)
  {
    return (first.getUTCseconds()            == second.getUTCseconds()            &&
	    first.getUTC16nanosecondcycles() == second.getUTC16nanosecondcycles());
  }

 
  /**
   * Not equal operator for UTC times.
   *
   * \param  first       UTC time
   * \param  second      UTC time
   * \result             true if first UTC time not equal second UTC time; else false
   */
  inline bool operator!=(const JDAQUTCExtended& first, const JDAQUTCExtended& second)
  {
    return (first.getUTCseconds()            != second.getUTCseconds()            ||
	    first.getUTC16nanosecondcycles() != second.getUTC16nanosecondcycles());
  }
}

#endif
