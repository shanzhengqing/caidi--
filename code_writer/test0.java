// Java��˿��ʾ������

import .util.List;
import .util.ArrayList;

// ʵ���࣬��Ӧ���ݱ�user
class User {
    private int id;
    private String name;
    private int age;

    public User(int id, String name, int age) {
        this.id = id;
        this.name = name;
        this.age = age;
    }

    // getter��setter����ʡ��
}

// DAO�����ݷ��ʶ��󣩲㣬�������ݿ���ز���
class UserDao {
    // ģ�����ݿ��е����ݴ洢
    private static List<User> userList = new ArrayList<>();

    static {
        User user1 = new User(1, "����", 20);
        User user2 = new User(2, "����", 25);
        userList.add(user1);
        userList.add(user2);
    }

    // ��ȡ�����û���Ϣ
    public List<User> getAllUsers() {
        return userList;
    }

    // ����id��ȡ�û���Ϣ
    public User getUserById(int id) {
        for (User user : userList) {
            if (user.getId() == id) {
                return user;
            }
        }
        return null;
    }

    // �����û�
    public void addUser(User user) {
        userList.add(user);
    }

    // �����û���Ϣ
    public void updateUser(User newUser) {
        for (User user : userList) {
            if (user.getId() == newUser.getId()) {
                user.setName(newUser.getName());
                user.setAge(newUser.getAge());
                break;
            }
        }
    }

    // ɾ���û���Ϣ
    public void deleteUser(int id) {
        for (User user : userList) {
            if (user.getId() == id) {
                userList.remove(user);
                break;
            }
        }
    }
}

// ����㣬������ҵ���߼�
class UserService {
    private UserDao userDao = new UserDao();

    // ��ȡ�����û���Ϣ
    public List<User> getAllUsers() {
        return userDao.getAllUsers();
    }

    // ����id��ȡ�û���Ϣ
    public User getUserById(int id) {
        return userDao.getUserById(id);
    }

    // �����û�
    public void addUser(User user) {
        userDao.addUser(user);
    }

    // �����û���Ϣ
    public void updateUser(User newUser) {
        userDao.updateUser(newUser);
    }

    // ɾ���û���Ϣ
    public void deleteUser(int id) {
        userDao.deleteUser(id);
    }
}

// ���������������������Ӧ
class UserController {
    private UserService userService = new UserService();

    // ��ȡ�����û���Ϣ
    public List<User> getAllUsers() {
        return userService.getAllUsers();
    }

    // ����id��ȡ�û���Ϣ
    public User getUserById(int id) {
        return userService.getUserById(id);
    }

    // �����û�
    public void addUser(User user) {
        userService.addUser(user);
    }

    // �����û���Ϣ
    public void updateUser(User newUser) {
        userService.updateUser(newUser);
    }

    // ɾ���û���Ϣ
    public void deleteUser(int id) {
        userService.deleteUser(id);
    }
}

// �����
public class Main {
    public static void main(String[] args) {
        UserController userController = new UserController();

        // �����û�
        User user3 = new User(3, "����", 30);
        userController.addUser(user3);

        // ��ȡ�����û���Ϣ
        List<User> userList = userController.getAllUsers();
        for (User user : userList) {
            System.out.println(user.getId() + ": " + user.getName() + ", " + user.getAge());
        }

        // �����û���Ϣ
        User user2 = userController.getUserById(2);
        user2.setName("������");
        userController.updateUser(user2);

        // ɾ���û���Ϣ
        userController.deleteUser(1);
    }
}