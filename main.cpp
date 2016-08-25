#include <iostream>
#include <string>
#include <ctime>

using namespace std;

class Card // How # and suit for cards are stored
{
private:
    int m_suitnum;
    string m_suit;
    int m_num;
  
public:
  
  Card(Card *ptr = NULL)
  {
    next = ptr;
  };
  
  Card *next;
  
  void readCard()
  {
    switch (m_num)
    {
      case 1:
        cout << "Ace";
        break;
      case 2:
      case 3:
      case 4:
      case 5:
      case 6:
      case 7:
      case 8:
      case 9:
      case 10:
        cout << m_num;
        break;
      case 11:
        cout << "Jack";
        break;
      case 12:
        cout << "Queen";
        break;
      case 13:
        cout << "King";
        break;
      default:
        cout << "Corrupted Card! RESTART";
        break;
    };
    
    cout << " of " << m_suit;
  };
  
  void init(int suit, int num) // Initialize the card
  {
    m_suitnum = suit;
    switch (m_suitnum)
    {
      case 1:
        m_suit = "Spades";
        break;
      case 2:
        m_suit = "Clubs";
        break;
      case 3:
        m_suit = "Diamonds";
        break;
      case 4:
        m_suit = "Hearts";
        break;
      default:
        cout << "Unknown suit value: RESTART";
        break;
    };
    m_num = num;
  };
  
  int returnNum() // Accessing private variables
  {
    return m_num;
  };
  
  int returnSuitnum()
  {
    return m_suitnum;
  };
};

int main ()
{
  cout << "It's time to play...   GO FISH! *cue applause from audience*\n\nYou know the rules! Press enter to play!\n\n";
  
  return 0;
};
